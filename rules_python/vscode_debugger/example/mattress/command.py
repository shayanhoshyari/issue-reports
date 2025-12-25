import sys
import time

def main() -> None:
    import bazel_debugpy.connect
    print(__file__)
    print(f"Hello form submodule: {sys.argv[1]}")
    time.sleep(2)

if __name__ == "__main__":
    main()
