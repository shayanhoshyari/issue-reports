import os

def main():
    print(f"{yellow_color}runfiles root is:{reset_color} {os.path.dirname(os.getcwd())}")

    import cowsay
    print(f'{pass_color}Import "cowsay" was successful{reset_color}')

    try:
        import google.cloud.storage
        print(f'{pass_color}Import "google.cloud.storage" was successful{reset_color}')
    except ImportError:
        print(f'{fail_color}Import "google.cloud.storage" Failed!{reset_color}')

fail_color = '\033[91m'
pass_color = '\033[92m'
yellow_color = '\033[93m'
reset_color = '\033[0m'

if __name__ == "__main__":
    main()