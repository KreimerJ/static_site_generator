from block_markdown_syntax import markdown_to_blocks
from copy_static import clean_public_and_copy_static_files


def extract_title(markdown_text: str):
    for block in markdown_to_blocks(markdown_text):
        if block.startswith("# "):
            return block.removeprefix("# ").strip()
        else:
            raise ValueError("no title found")


def main():
    clean_public_and_copy_static_files()


if __name__ == "__main__":
    main()
