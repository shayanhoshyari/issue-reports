import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

def main() -> None:
    env = os.environ.copy()

    debugpy = importlib.import_module("debugpy")
    pydevd = debugpy.server.api.pydevd
    setup = pydevd.SetupHolder.setup
    info = {
        "ppid": os.getpid(),
        "sys_path": str(Path(debugpy.__file__).resolve().parents[1]),
        "client": setup.get("client"),
        "port": setup.get("port"),
        "client_access_token": setup.get("client-access-token"),
    }
    env["bzl_pydev_config"] = info_json = json.dumps(info)
    env["PYTHONBREAKPOINT"] = "debugpy.breakpoint"

    args = ["bazel", sys.argv[1], "--@rules_python//python/config_settings:debugger=//:attach", f"--test_env=bzl_pydev_config={info_json}", sys.argv[2]]
    os.execvpe(args[0], args, env)
    # subprocess.run(args, env=env)



if __name__ == "__main__":
    main()