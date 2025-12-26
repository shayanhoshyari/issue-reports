import mattress
import sys

if __name__ == "__main__":
    print([p for p in sys.path if "debugpy" in p])
    mattress.announce("Constantine")