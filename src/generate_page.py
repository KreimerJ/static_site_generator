import os

from block_markdown_syntax import extract_title, markdown_to_html_node


def generate_page(
    from_path: str, template: str, destination_path: str, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {destination_path} using {template}")

    with open(from_path, "r") as file_to_read:
        markdown_text: str = file_to_read.read()

    with open(template, "r") as file_to_read:
        template_text: str = file_to_read.read()

    markdown_to_html_string: str = (
        markdown_to_html_node(markdown_text)
        .to_html()
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    template_text = template_text.replace(
        "{{ Title }}", extract_title(markdown_text)
    ).replace("{{ Content }}", markdown_to_html_string)

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    with open(destination_path, "w") as file_to_write:
        file_to_write.write(template_text)


def generate_page_recursively(
    dir_path_content: str, template_path: str, destination_dir_path: str, basepath: str
) -> None:
    for file in os.listdir(dir_path_content):
        file_path_content: str = os.path.join(dir_path_content, file)
        if os.path.isfile(file_path_content):
            destination_file_path: str = os.path.join(
                destination_dir_path, file.replace(".md", ".html")
            )
            generate_page(
                file_path_content, template_path, destination_file_path, basepath
            )
        else:
            new_destination_dir_path = os.path.join(destination_dir_path, file)
            os.makedirs(new_destination_dir_path, exist_ok=True)
            generate_page_recursively(
                file_path_content, template_path, new_destination_dir_path, basepath
            )
