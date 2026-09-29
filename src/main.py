import os

from copy_static import clean_public_and_copy_static_files
from generate_page import generate_page_recursively


def main():
    source_dir: str = os.path.join(os.getcwd(), "content")
    template: str = os.path.join(os.getcwd(), "template.html")
    public_dir: str = os.path.join(os.getcwd(), "public")

    clean_public_and_copy_static_files()
    generate_page_recursively(source_dir, template, public_dir)


if __name__ == "__main__":
    main()
