from pathlib import Path
import subprocess
import sys
import time

def announce(name: str) -> None:
    print(f"Hello from main module: {name}")
    # does not work
    # breakpoint()

    subprocess.check_call([sys.executable, "-m", "mattress.command", name])
    # subprocess.check_call([sys.executable, Path(__file__).with_name("command.py"), name])

    # main()
    time.sleep(2)
    print("We are now done!")