import os
import shutil


def test():
    print(os.getcwd())
    public_dir = os.path.join(os.getcwd(), "public")
    if os.path.exists(public_dir):
        os.chdir(public_dir)
        print(f"dir = {os.getcwd()}")


def clean_previous_public_and_copy():
    public_dir = os.path.join(os.getcwd(), "public")
    static_dir = os.path.join(os.getcwd(), "static")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir, ignore_errors=True)
        print(f"removed {public_dir}")
        os.mkdir(public_dir)
        print(f"created{public_dir}")

    copy_static_files(static_dir, public_dir)


def copy_static_files(source_path, destination_path):
    if not os.path.exists(source_path):
        return

    for item in os.listdir(source_path):
        if os.path.isfile(item):
            copy_static_files(os.path.join(source_path, item), destination_path)
            print(
                f"copied {item}, path = {os.path.join(source_path, item)}, destination = {destination_path}"
            )
        else:
            shutil.copy(os.path.join(source_path, item), destination_path)
            print(
                f"copied {item}, path = {os.path.join(source_path, item)}, destination = {destination_path}"
            )


def main():
    test()


if __name__ == "__main__":
    main()
