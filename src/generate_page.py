import os

from block_markdown_syntax import extract_title, markdown_to_html_node


def generate_page(from_path: str, template: str, destination_path: str) -> None:
    print(f"Generating page from {from_path} to {destination_path} using {template}")

    with open(from_path, "r") as file_to_read:
        markdown_text: str = file_to_read.read()

    with open(template, "r") as file_to_read:
        template_text: str = file_to_read.read()

    markdown_to_html_string: str = markdown_to_html_node(markdown_text).to_html()
    template_text = template_text.replace(
        "{{ Title }}", extract_title(markdown_text)
    ).replace("{{ Content }}", markdown_to_html_string)

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    with open(destination_path, "w") as file_to_write:
        file_to_write.write(template_text)
