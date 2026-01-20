"""
A replacement of py_image_layer that does not suffer from the following:

- https://github.com/bazel-contrib/rules_python/issues/3388
- https://github.com/bazel-contrib/tar.bzl/issues/16
- https://github.com/bazel-contrib/rules_python/issues/3439

The output are two tars that their union makes the .runfiles folder
of a py_binary. So that they can be added as layers to a dockerfile

Assuming that the py_binary is at //coffee/cup:exe, the layers are as follows:

    ```
    _main/coffee/cup/
        # Bash script launcher (calls: python _exe_bootstrap_stage2.py)
        # The `.venv/lib/site-packages` and `_main` will be added to path.
        exe
        _exe_bootstrap_stage2.py

        # Any files under py_binary or its deps that belong to this MODULE
        exe.py
        lib.py
        ...

        # .venv style structure for deps
        _exe.venv/
            # Python interpreter used to launch
            bin/python3
            lib/
                python3.13/
                site-packages/
                    # Symlinks to all dependency .py files (e.g. torch, ...)
                    # (these symlinks typically point up to the 'rules_...' folders below)

    # All files from external Bazel MODULEs/REPOs:
    rules_python++pip+pypi_platforms_inference_gitops_312_typing_inspection/
    site-packages/
        ...
    rules_python++pip+pypi_platforms_inference_gitops_312_wrapt/
    site-packages/
        ...
    ```


We add everything under _main to one layer, and others to another layer.
main is meant to be light and just files from this module that change often
(or just symlinks under .venv) while others are from deps, very heavy and change less often.

"""

load("@rules_python//python:defs.bzl", "PyRuntimeInfo")

# Any file matching these groups will be added to its own layer.
# The reason is that these packages are huge, and putting them in
# separate layers, make those large layers cacheable.
#
# Keep small otherwise will see perf penalty.
# The dist_info stuff still goes to the .external. group, but that
# is okay. The idea is, if I change filelock, the torch layer should
# not rebuild. But if I change torch, external layer rebuild is okay.
_LAYER_GROUPS = {
    "torch": "/site-packages/torch/",
    "nvidia": "/site-packages/nvidia/",
}

_ALL_GROUPS = ["main", "external"] + list(_LAYER_GROUPS.keys())

def _file_group(file):
    if not file.path.startswith("external/"):
        return "main"

    for group, pattern in _LAYER_GROUPS.items():
        if pattern in file.short_path:
            return group

    return "external"

def _file_manifest_line(file, group):
    """
    Convert a runfile to a manifest line.
    """
    if file.is_symlink:
        # This file is a symlink, just write the link itself.
        return json.encode({"path": file.path, "short": file.short_path, "link": "disk", "group": group})

    # Actual file, resolve it and write the actual file.
    return json.encode({"path": file.path, "short": file.short_path, "link": "no", "group": group})

def _symlink_manifest_line(file, group):
    """
    Convert a symlink to a manifest line.
    """

    # This is a link, but don't trust the value, use the link provided here.
    # Provided value is a short path.
    # https://bazel.build/rules/lib/builtins/SymlinkEntry
    return json.encode({"path": file.target_file.short_path, "short": file.path, "link": "path", "group": group})

def _tar_runfiles(ctx):
    """
    Implementation of tar_runfiles
    """
    py_binary = ctx.attr.py_binary
    entrypoint = ctx.attr.entrypoint

    # 1. Write the manifest
    default_info = py_binary[DefaultInfo]

    runfiles = {g: [] for g in _ALL_GROUPS}
    manifest_contents = {g: [] for g in _ALL_GROUPS}

    # These are ctx.actions.add_file/symlinks
    for f in default_info.default_runfiles.files.to_list():
        group = _file_group(f)
        line = _file_manifest_line(f, group)
        runfiles[group].append(f)
        manifest_contents[group].append(line)

    # These are runfiles(symlinks = ...)
    # see reason why we have both: https://github.com/bazel-contrib/rules_python/issues/3439#issuecomment-3638127812
    for f in default_info.default_runfiles.symlinks.to_list():
        # group = main is a heuristic, symlinks are mainly from py_binary that makes the .venv
        line = _symlink_manifest_line(f, "main")
        manifest_contents["main"].append(line)

    tarballs = {}
    manifests = {}
    for group in _ALL_GROUPS:
        # Write the manifest for that group
        manifests[group] = ctx.actions.declare_file("{}.{}.manifest".format(ctx.attr.name, group))
        ctx.actions.write(
            output = manifests[group],
            content = "\n".join(manifest_contents[group]),
        )

        # Execute the tar command
        tarballs[group] = ctx.actions.declare_file("{}.{}.tar".format(ctx.attr.name, group))

        ctx.actions.run(
            outputs = [tarballs[group]],
            inputs = [manifests[group]] + runfiles[group],
            executable = ctx.executable._tool,
            arguments = [
                manifests[group].path,
                tarballs[group].path,
                "--group",
                group,
                "--entrypoint",
                entrypoint,
                "--py-binary",
                py_binary.files_to_run.executable.short_path,
            ],
        )

    return [
        # Only add tars to the output, otherwise oci image building fails
        # as it is gonna receive manifest as input
        DefaultInfo(
            files = depset(tarballs.values()),
        ),

        # Add named outputs for debugging, e.g. I can just build manifest
        # with --output_group=manifests.
        OutputGroupInfo(
            manifests = depset(manifests.values()),
            tarballs = depset(tarballs.values()),
        ),
    ]

tar_runfiles = rule(
    implementation = _tar_runfiles,
    attrs = {
        "py_binary": attr.label(
            doc = "py_binary target whose runfiles to iterate over.",
            providers = [PyRuntimeInfo],
        ),
        "entrypoint": attr.string(
            doc = " We will make a entrypoint executable and entrypoint.runfiles for the py_binary runfiles.",
            default = "entrypoint",
        ),
        "_tool": attr.label(
            default = Label(":tar_runfiles"),
            executable = True,
            cfg = "exec",
        ),
    },
    doc = "A rule which iterates over all runfiles of a given py_binary. Replacement for py_image_layer that supports symlinks.",
)
