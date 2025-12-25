import importlib
import json
import os
from pathlib import Path
import shlex
import argparse
from ._shared import PydecConfig

def main() -> None:
    parser = argparse.ArgumentParser(description="Launch bazel debugpy with test or run.")
    parser.add_argument('mode', choices=['test', 'run'], help='Choose whether to run a bazel test or run.')
    parser.add_argument('target', help='The bazel target to test or run (e.g., //foo:bar)')
    parser.add_argument('args', help='Optional args to pass to executable as single string')
    parser.add_argument('--bazel', default="bazel", help='Optional path to bazel')
    parser.add_argument('--hub-name', default="pypi", help='Name used for pip.parse that contains this package')
    args = parser.parse_args()

    env = os.environ.copy()

    debugpy = importlib.import_module("debugpy")
    pydevd = debugpy.server.api.pydevd
    setup = pydevd.SetupHolder.setup
    info = PydecConfig(
        ppid = os.getpid(),
        sys_path = str(Path(debugpy.__file__).resolve().parents[1]),
        port = setup.get("port"),
        client_access_token = setup.get("client-access-token"),
    )
    info_json = json.dumps(info)
    env["PYTHONBREAKPOINT"] = "debugpy.breakpoint"

    others = shlex.split(args.args) if args.args else []

    cmd = [
        args.bazel,
        args.mode,
        f"--@rules_python//python/config_settings:debugger=@{args.hub_name}//bazel_debugpy",
        args.target,
    ]
    if args.mode == "test":
        cmd.append(f"--test_env=bzl_pydev_config={info_json}")
    else:
        env["bzl_pydev_config"] = info_json
    cmd.extend(others)
    os.execvpe(cmd[0], cmd, env)



if __name__ == "__main__":
    main()