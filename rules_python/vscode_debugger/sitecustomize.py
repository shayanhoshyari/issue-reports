import importlib
import json
import os
import sys
from typing import TypedDict, cast


class PydecConfig(TypedDict):
    sys_path: str
    client: str
    port: int
    client_access_token: str
    ppid: int


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
    # pydevd = debugpy.server.api.pydevd
    # pydevd.SetupHolder.setup = {
    #     "ppid": pydev_config["ppid"],
    #     "client": pydev_config["client"],
    #     "port": pydev_config["port"],
    #     "client-access-token": pydev_config["client_access_token"],
    # }
    debugpy.connect([pydev_config["client"], pydev_config["port"]], access_token=pydev_config["client_access_token"])
    debugpy.wait_for_client()

    print("Connection complete!")


main()