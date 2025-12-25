from typing import TypedDict

class PydecConfig(TypedDict):
    sys_path: str
    port: int
    client_access_token: str
    ppid: int
