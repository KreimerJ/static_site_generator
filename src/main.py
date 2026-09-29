import os

from copy_static import clean_public_and_copy_static_files
from generate_page import generate_page


def main():
    source_index: str = os.path.join(os.getcwd(), "content/index.md")
    template: str = os.path.join(os.getcwd(), "template.html")
    index_html: str = os.path.join(os.getcwd(), "public/index.html")

    clean_public_and_copy_static_files()
    generate_page(source_index, template, index_html)


if __name__ == "__main__":
    main()
