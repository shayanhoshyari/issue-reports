import importlib
import json
import os
import sys
from typing import cast
from ._shared import PydecConfig


def main() -> None:
    maybe_pydev_config = os.getenv("bzl_pydev_config")
    if not maybe_pydev_config:
        print("bzl_pydev_config not found")
        return

    pydev_config = cast(PydecConfig, json.loads(maybe_pydev_config))
    try:
        if pydev_config["sys_path"] not in sys.path:
            sys.path.append(pydev_config["sys_path"])
        debugpy = importlib.import_module("debugpy")
    except Exception:
        print("Could not import debupy")
        return

    if debugpy.is_client_connected():
        print("debugpy client already connected.")
        return

    # Connect
    print("Connecting to debugpy")
    debugpy.connect(
        pydev_config["port"],
        access_token=pydev_config["client_access_token"],
        parent_session_pid=pydev_config["ppid"],
    )
    debugpy.wait_for_client()

    print("Connection complete!")

    # update debug connection, so processes this process launches show
    # up correctly.
    pydev_config["ppid"] = os.getpid()
    os.environ["bzl_pydev_config"] = json.dumps(pydev_config)


main()