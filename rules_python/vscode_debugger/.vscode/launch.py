import importlib
import json
import os
import shlex
import argparse

def main() -> None:
    parser = argparse.ArgumentParser(description="Launch bazel debugpy with test or run.")
    parser.add_argument('mode', choices=['test', 'run'], help='Choose whether to run a bazel test or run.')
    parser.add_argument('target', help='The bazel target to test or run (e.g., //foo:bar)')
    parser.add_argument('args', help='Optional args to pass to executable as single string')
    args = parser.parse_args()

    env = os.environ.copy()

    debugpy = __import__("debugpy") # provided by vscode
    setup = debugpy.server.api.pydevd.SetupHolder.setup
    info = {
        "sys_path" : os.path.dirname(os.path.dirname(os.path.normpath(debugpy.__file__))),
        "ppid": os.getpid(),
        "port": setup.get("port"),
        "client_access_token": setup.get("client-access-token"),
    }
    info_json = json.dumps(info)

    others = shlex.split(args.args) if args.args else []

    cmd = [
        "./bazel",
        args.mode,
        f"--@rules_python//python/config_settings:debugger=//:debugpy",
        args.target,
    ]
    cmd.append(f"--test_env=bzl_pydev_config={info_json}")
    env["bzl_pydev_config"] = info_json

    cmd.extend(others)
    os.execvpe(cmd[0], cmd, env)

if __name__ == "__main__":
    main()
