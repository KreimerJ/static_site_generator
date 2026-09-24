import os
import shutil


def clean_public_and_copy_static_files():
    public_dir = os.path.join(os.getcwd(), "public")
    static_dir = os.path.join(os.getcwd(), "static")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir, ignore_errors=True)
        os.mkdir(public_dir)
    else:
        os.mkdir(public_dir)

    copy_static_files(static_dir, public_dir)


def copy_static_files(source_path, destination_path):
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"source path {source_path} does not exist")

    for item in os.listdir(source_path):
        new_item_path = os.path.join(source_path, item)
        new_destination_path = os.path.join(destination_path, item)
        if os.path.isdir(new_item_path):
            os.mkdir(new_destination_path)
            copy_static_files(new_item_path, new_destination_path)
        else:
            shutil.copy(new_item_path, destination_path)


def main():
    clean_public_and_copy_static_files()


if __name__ == "__main__":
    main()
