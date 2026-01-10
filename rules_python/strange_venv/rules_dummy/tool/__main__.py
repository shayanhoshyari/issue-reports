import os

def main():
    print(f"runfiles root is: {os.path.dirname(os.getcwd())}")

    import platforms.dev_tools.multitool
    print("Import was successful")

if __name__ == "__main__":
    main()