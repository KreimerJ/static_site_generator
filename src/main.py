import os
import sys

from copy_static import clean_public_and_copy_static_files
from generate_page import generate_page_recursively


def main():
    basepath: str = ""
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    source_dir: str = os.path.join(os.getcwd(), "content")
    template: str = os.path.join(os.getcwd(), "template.html")
    docs_dir: str = os.path.join(os.getcwd(), "docs")

    clean_public_and_copy_static_files(docs_dir)
    generate_page_recursively(source_dir, template, docs_dir, basepath)


if __name__ == "__main__":
    main()
