import json
import os
import sys
from typing import cast, TypedDict

class PydecConfig(TypedDict):
    sys_path : str
    port: int
    client_access_token: str
    ppid: int


def main() -> None:
    maybe_pydev_config = os.getenv("bzl_pydev_config")
    if not maybe_pydev_config:
        # We only need this for first launched process.
        #
        # After that pydevd will patch the right functions and we don't
        # need this anymore.
        return

    pydev_config = cast(PydecConfig, json.loads(maybe_pydev_config))

    print("importing debugpy from", pydev_config["sys_path"])
    sys.path.insert(0, pydev_config["sys_path"])
    debugpy = __import__("debugpy")

    # Connect
    print("Connecting to debugpy")
    # this is default, just just in case.
    # debugpy.configure(subProcess=True)
    debugpy.connect(
        pydev_config["port"],
        access_token=pydev_config["client_access_token"],
        parent_session_pid=pydev_config["ppid"],
    )
    print("Connection complete!")

    # After that pydevd will patch the right functions and we don't
    # need this anymore.
    del os.environ["bzl_pydev_config"]


main()