"""
Launcher script for .vscode.

This will run bazel run / test and inject "bzl_pydev_config" env var that allows the 
parent process to connect back to debugpy.

This file just can run with any python and is not managed by Bazel. It is referenced
from launch.json.
"""

import json
import os
import shlex
import argparse
import sys

def main() -> None:
    parser = argparse.ArgumentParser(description="Launch bazel debugpy with test or run.")
    parser.add_argument('mode', choices=['test', 'run'], help='Choose whether to run a bazel test or run.')
    parser.add_argument('args', help='The bazel target to test or run (e.g., //foo:bar) and any additional args')
    args = parser.parse_args()

    # Import debugpy, provided by vscode
    try:
        import debugpy # type: ignore[import-not-found]
        # This is needed because it runs force_pydevd that does some path manipulation
        # See https://github.com/microsoft/debugpy/blob/main/src/debugpy/server/__init__.py
        import debugpy._vendored # type: ignore[import-not-found]

        # SetupHolder from this module: https://github.com/microsoft/debugpy/blob/main/src/debugpy/_vendored/pydevd/pydevd.py
        from pydevd import SetupHolder # type: ignore[import-not-found]
        setup = SetupHolder.setup
    except ImportError as exc:
        print(f"You must run launch.py as vscode debug target, err: {exc}")
        sys.exit(-1)

    assert debugpy.__file__ is not None, "You must run launch.py as vscode debug target" # for mypy
    info = {
        "sys_path" : os.path.dirname(os.path.dirname(os.path.normpath(debugpy.__file__))),
        "port": setup.get("port"),
        "client_access_token": setup.get("client-access-token"),
        "parent_session_pid" : os.getpid(),
    }
    info_json = json.dumps(info)

    bzl_args = shlex.split(args.args)
    assert len(bzl_args) >= 1, "at least one arg should be given, which is the target to run"

    # Command line arguments
    cmd = [
        "./bazel",
        args.mode,
        # This will install the hook that reads the env var to connect back
        # to the debugger.
        f"--@rules_python//python/config_settings:debugger=//.vscode/debugpy:attach",
        # This is necessary so that the the debugger hits breakpoints in original
        # source and not the symlinks in bazel output.
        "--test_env=PYDEVD_RESOLVE_SYMLINKS=1",
        # This is necessary so tests can access the connect back env var.
        f"--test_env=bzl_pydev_config={info_json}",
        bzl_args[0],
    ]
    if bzl_args[1:]:
        # Extra arguments, only useful for mode == test
        cmd.append("--")
        cmd.extend(bzl_args[1:])

    # Env vars
    env = {
        **os.environ.copy(),
        # Similar to test_env but for run.
        "bzl_pydev_config" : info_json,
        "PYDEVD_RESOLVE_SYMLINKS" : "1",
    }

    # Run Bazel.
    os.execvpe(cmd[0], cmd, env)

if __name__ == "__main__":
    main()
