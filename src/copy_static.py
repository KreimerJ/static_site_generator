import os
import shutil


def clean_public_and_copy_static_files(destination_dir: str) -> None:
    static_dir: str = os.path.join(os.getcwd(), "static")
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir, ignore_errors=True)
        os.mkdir(destination_dir)
    else:
        os.mkdir(destination_dir)
    copy_static_files(static_dir, destination_dir)


def copy_static_files(source_path, destination_path) -> None:
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"source path {source_path} does not exist")
    for item in os.listdir(source_path):
        new_item_path: str = os.path.join(source_path, item)
        new_destination_path: str = os.path.join(destination_path, item)
        if os.path.isdir(new_item_path):
            os.mkdir(new_destination_path)
            copy_static_files(new_item_path, new_destination_path)
        else:
            shutil.copy(new_item_path, destination_path)
