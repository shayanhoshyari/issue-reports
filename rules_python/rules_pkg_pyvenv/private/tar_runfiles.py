#!/usr/bin/env python3

"""
Script to create a tar archive.

The manifest should be a text file with lines formatted as:
    <path> | <short path> | <is_link>  | <group>
    ...

Usage:
    python tar_runfiles.py manifest output [--group ...]
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import tarfile
import uuid
from pathlib import Path
from typing import Literal, cast


def main() -> None:
    parser = argparse.ArgumentParser(description="Create two tars ('local' and 'external') based on a manifest.")
    parser.add_argument("manifest", help="Path to manifest file")
    parser.add_argument("output", help="Output tar file for 'local' group")
    parser.add_argument("--group", required=True, help="groups to include in the tar")
    parser.add_argument("--entrypoint", required=True, help="Path to put the entrypoint.")
    parser.add_argument("--py-binary", required=True, help="Path to the py_binary main exe within runfiles")
    args = parser.parse_args()

    entrypoint = Path("/") / cast(str, args.entrypoint)  # if relative make abs
    output = cast(str, args.output)
    manifest_path = Path(args.manifest)
    target_group = cast(str, args.group)
    py_binary = Path(args.py_binary)

    # A tmp path for scratch files. Since we use bazel and sanboxing, just using
    # pwd is enough
    tmp = Path.cwd() / "tmp"
    tmp.mkdir()

    # Read the runfiles
    files = read_runfiles(manifest_path)

    # Helper to get files that need to go to tarball. Most files just come from bazel. Only the ones with link=path
    # need an actual symlink made on the fly.
    builder = LinkBuilder(tmp)

    with tarfile.open(output, "w") as tar_stream:
        # 1. Add all the runfiles
        for file in files:
            if target_group is not None and file.group != target_group:
                # This file is not meant for this layer.
                continue

            source = builder.get_src(file)
            # destination is just adding the runfile under the docker work directory.
            arcname = entrypoint.parent / f"{entrypoint.name}.runfiles" / file.runfile_path

            tar_stream.add(source, arcname=arcname, recursive=False)

        # 2. For the main layer, also add the entrypoint.
        if target_group == "main":
            run_sh = tmp / "entrypoint.sh"

            run_content = _ENTRYPOINT.format(py_binary_exe=py_binary)
            run_sh.write_text(run_content)
            os.chmod(run_sh, 0o755)

            tar_stream.add(run_sh, arcname=entrypoint, recursive=False)


@dataclasses.dataclass
class Runfile:
    """Python representation of a bazel runfile"""

    # Path under bazel execroot
    path: str

    # Path under runfile (exectuable.runfiles folder).
    runfile_path: str

    # no: this is not a link, resolve actual file and write it
    # disk: it is a link, and the link value is what is actually in the file on disk
    # path: This is a link, and the value on disk is useless. Make a symlink poitning to file.path
    #  assuming path is a runfile path too.
    #
    # Refs
    # - https://bazel.build/rules/lib/builtins/File#is_symlink
    # - https://bazel.build/rules/lib/builtins/SymlinkEntry
    link: Literal["no", "disk", "path"]

    # either external or main. It says if the file comes from root bazel MODULE, or from dependencies
    # We process them separately so that the more changing things (from root MODULE) go to separate
    # tar and hence separate docker image layer. As they are lighter (~100 MB) and change more often.
    group: str


def read_runfiles(manifest: Path) -> list[Runfile]:
    """
    Read all the runfiles from the manifest written by tar_runfiles.bzl
    """
    files = list[Runfile]()
    with manifest.open("r") as stream:
        while line := stream.readline():
            line = line.strip()
            if not line:
                continue
            val = json.loads(line)

            # val["link"] == "path" means path is a runfile path too. Bazel is relative to _main, we do relative to
            # runfile root, so add main.
            val["path"] = os.path.normpath(os.path.join("_main", val["path"])) if val["link"] == "path" else val["path"]

            file = Runfile(
                path=val["path"],
                # Bazel is relative to _main, we do relative to runfile root, so add main.
                runfile_path=os.path.normpath(os.path.join("_main", val["short"])),
                link=val["link"],
                group=val["group"],
            )
            files.append(file)
    return files


class LinkBuilder:
    """
    A class that stores import_path (for python) to file path under rules_...
    with external group.

    We will use "maybe_rel_link" to query if a file in main that still has
    is_symlink = False, can actually be a symlink.
    """

    def get_src(self, file: Runfile) -> Path:
        """
        Get the source file that needs to be added to the tar.
        """
        if file.link == "disk":
            # This file is a symlink, so we know we need to just add the link
            # and preserve it. Do not resolve the link.
            return Path(file.path)

        if file.link == "no":
            # File that we need to write the original file in the tarball.
            return Path(file.path).resolve()

        if file.link == "path":
            to_runfile = file.path  # I abused meaning of path here, sorry :(

            # dirname intentional,  links are relative to parent folder
            venv_runfile_parent = os.path.dirname(file.runfile_path)

            # using os.path.relpath is intentional (compared to Path.relative_path)
            # as it handles something like relpath(a/b/c, a/d) = ../b/c
            # How to go from venv_runfile_parent to external_runfile
            link_target = os.path.relpath(to_runfile, venv_runfile_parent)

            # Make a symlink and return it so it can be added to the tar
            result = self.tmp / str(uuid.uuid4())  # just some unique temp file
            os.symlink(link_target, result)
            return result

        raise ValueError(f"invalid mode {file.link}")

    def __init__(self, tmp: Path) -> None:
        self.tmp = tmp


# The template for creating a entrypoint in the main/ tarball (layer).
# User can just run entrypoint as the image entrypoint for simplicity.
#
# - RUNFILES_DIR must be set as bazel entrypoint without it won't work. Must be abs path.
# - py_binary_exe is the short_path of actual py_binary startup script from bazel.
_ENTRYPOINT = """#!/bin/bash
set -ex
export RUNFILES_DIR=$(realpath "$0.runfiles")
exec "${{RUNFILES_DIR}}/_main/{py_binary_exe}" "$@"
"""

if __name__ == "__main__":
    main()
