import re
from collections.abc import Callable

from src.textnode import TextNode, TextType


def delimiter_splitter_helper(
    text: str, delimiter: str, text_type: TextType
) -> list[TextNode]:
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
            new_nodes.extend(
                delimiter_splitter_helper(old_node.text, delimiter, text_type)
            )
    return new_nodes


def extract_markdown_image(text: str) -> list[tuple]:
    matches: list[tuple] = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_link(text: str) -> list[tuple]:
    matches: list[tuple] = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def links_splitter_helper(
    node: TextNode,
    extractor: Callable[[str], list[tuple[str, str]]],
    image_link_format: str = "",
) -> list[TextNode]:
    text = node.text
    text_type = TextType.LINK
    if image_link_format:
        text_type = TextType.IMAGE_LINK
    text_nodes: list[TextNode] = []
    extractions: list[tuple[str, str]] = extractor(text)
    remaning_text: str = text
    if not extractions:
        return [node]
    for alt_text, url in extractions:
        marker: str = f"{image_link_format}[{alt_text}]({url})".strip()
        text_parts: list[str] = remaning_text.split(marker, 1)
        if text_parts[0]:
            text_nodes.append(TextNode(text_parts[0], TextType.PLAIN))
        text_nodes.append(TextNode(alt_text, text_type, url))
        remaning_text = text_parts[1]
    if remaning_text:
        text_nodes.append(TextNode(remaning_text, TextType.PLAIN))
    return text_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            new_nodes.extend(links_splitter_helper(node, extract_markdown_image, "!"))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            new_nodes.extend(links_splitter_helper(node, extract_markdown_link))
    return new_nodes
