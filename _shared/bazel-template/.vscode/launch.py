"""
Launcher script for .vscode.

This file just can run with any python and is not managed by Bazel. It is referenced
from launch.json.
"""

import os
import shlex
import argparse
import sys
from typing import cast

def main() -> None:
    parser = argparse.ArgumentParser(description="Launch bazel debugpy with test or run.")
    parser.add_argument('mode', choices=['test', 'run'], help='Choose whether to run a bazel test or run.')
    parser.add_argument('args', help='The bazel target to test or run (e.g., //foo:bar) and any additional args')
    args = parser.parse_args()

    # Import debugpy, provided by vscode
    try:
        # This is needed because it runs force_pydevd that does some path manipulation
        # See https://github.com/microsoft/debugpy/blob/main/src/debugpy/server/__init__.py
        import debugpy._vendored # type: ignore[import-not-found]

        # https://github.com/microsoft/debugpy/blob/main/src/debugpy/_vendored/pydevd/_pydev_bundle/pydev_monkey.py
        # for usage see https://github.com/microsoft/debugpy/blob/main/src/debugpy/_vendored/pydevd/pydevd.py
        # this is where pydev patches os and subprocess functions to handle new launched processes
        from _pydev_bundle import pydev_monkey # type: ignore[import-not-found]
    except ImportError as exc:
        print(f"You must run launch.py as vscode debug target, err: {exc}")
        sys.exit(-1)


    # is_exec means if we are using os.exec API to replace this process.
    # I tried it to get rid of the top level process shown in vscode, but no luck.
    # when is_exec is used, one also needs to use pydev_monkey.send_process_about_to_be_replaced()
    patched_args = cast(list[str], pydev_monkey.patch_args(["python", "dummy.py"], is_exec=False))
    pydev_monkey.send_process_created_message()

    # Drop first and last one (python and dummy.py)
    patched_args = patched_args[1:-1]
    # Now ready to pass to rules_python. Shlex.join() does not work given how
    # rules python processes things in entrypoint. Not sure how bulletproof this
    # solution is.
    rules_python_interpretter_args = " ".join(patched_args)

    bzl_args = shlex.split(args.args)
    assert len(bzl_args) >= 1, "at least one arg should be given, which is the target to run"

    # Command line arguments
    cmd = [
        "./bazel",
        args.mode,
        # This is necessary so that the the debugger hits breakpoints in original
        # source and not the symlinks in bazel output.
        "--test_env=PYDEVD_RESOLVE_SYMLINKS=1",
        # This will make rules_python run the pydevd entrypoint that will connect back and then
        # run the actual entrypoint.
        f"--test_env=RULES_PYTHON_ADDITIONAL_INTERPRETER_ARGS={rules_python_interpretter_args}",
        bzl_args[0],
    ]
    if bzl_args[1:]:
        # Extra arguments, only useful for mode == run
        cmd.append("--")
        cmd.extend(bzl_args[1:])

    # Env vars
    env = {
        **os.environ.copy(),
        # Similar to test_env but for run.
        "RULES_PYTHON_ADDITIONAL_INTERPRETER_ARGS" : rules_python_interpretter_args,
        "PYDEVD_RESOLVE_SYMLINKS" : "1",
    }

    # Run Bazel.
    os.execvpe(cmd[0], cmd, env)
 
if __name__ == "__main__":
    main()
