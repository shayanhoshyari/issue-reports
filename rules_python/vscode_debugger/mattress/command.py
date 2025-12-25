import sys
import time

def main() -> None:
    print(f"Hello form submodule: {sys.argv[1]}")
    time.sleep(2)

if __name__ == "__main__":
    main()