import json
import os
import sys
from typing import cast, TypedDict

class PydecConfig(TypedDict):
    sys_path : str
    port: int
    client_access_token: str
    parent_session_pid : str


def main() -> None:
    maybe_pydev_config = os.getenv("bzl_pydev_config")
    if not maybe_pydev_config:
        # We only need this for first launched process.
        #
        # After that pydevd will patch the right functions and we don't
        # need this anymore.
        return

    pydev_config = cast(PydecConfig, json.loads(maybe_pydev_config))

    # Import debugpy!
    sys.path.insert(0, pydev_config["sys_path"])
    debugpy = __import__("debugpy")

    # Connect
    debugpy.configure(subProcess=True) # this is default, just just in case.
    debugpy.connect(
        pydev_config["port"],
        access_token=pydev_config["client_access_token"],
        parent_session_pid = pydev_config["parent_session_pid"],
    )

    # After that pydevd will patch the right functions and we don't
    # need this anymore to attach sub processes.
    del os.environ["bzl_pydev_config"]


main()