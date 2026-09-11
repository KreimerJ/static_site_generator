import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    delimiters: dict[str, TextType] = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }
    if delimiter not in delimiters:
        raise ValueError(f"Invalid delimiter {delimiter}")
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
        else:
            new_nodes.extend(splitter(old_node.text, delimiter, text_type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    pass


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    pass


def splitter(text: str, delimiter: str, text_type: TextType) -> list[TextNode]:
    text_nodes: list[TextNode] = []
    text_parts: list[str] = text.split(delimiter)
    if len(text_parts) % 2 == 0:
        raise ValueError(f"Invalid text nodes {text_parts}")

    for i, part in enumerate(text_parts):
        if part.strip() == "":
            continue
        if i % 2 == 0:
            text_nodes.append(TextNode(part, TextType.PLAIN))
        else:
            text_nodes.append(TextNode(part, text_type))
    return text_nodes


def extract_markdown_image(text: str) -> list[tuple]:
    matches: list[tuple] = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_link(text: str) -> list[tuple]:
    matches: list[tuple] = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
