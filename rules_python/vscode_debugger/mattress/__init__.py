import subprocess
import sys

def announce(name: str) -> None:
    print(f"Hello from main module: {name}")
    subprocess.check_call([sys.executable, "-m", "mattress.command", name])
    print("We are now done!")