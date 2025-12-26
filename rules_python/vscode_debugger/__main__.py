import os
import mattress
import sys

def _has_debugger_hook(path : str) -> bool:
    """Check if a path has our hook to start debugger installed"""
    for candidate in ["sitecustomize.py", "attach_debugpy.pth"]:
        if os.path.exists(os.path.join(path, candidate)):
            return True

    return False

if __name__ == "__main__":
    print("Debugger hook:", [p for p in sys.path if _has_debugger_hook(p)])
    mattress.announce("Constantine")
