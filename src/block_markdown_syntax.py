from enum import Enum

from htmlnode import HTMLNode
from inline_markdown_syntax import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    @property
    def html_tag(self):
        match self:
            case BlockType.PARAGRAPH:
                return "p"
            case BlockType.HEADING:
                return "h"
            case BlockType.CODE:
                return "pre"
            case BlockType.QUOTE:
                return "blockquote"
            case BlockType.UNORDERED_LIST:
                return "ul"
            case BlockType.ORDERED_LIST:
                return "ol"
            case _:
                raise ValueError(f"Unknown block type: {self}")


def markdown_to_blocks(markdown_text: str) -> list[str]:
    blocks: list[str] = [
        line.strip() for block in markdown_text.split("\n\n") if (line := block.strip())
    ]
    return blocks


def block_to_block_type(markdown_block_text: str) -> BlockType:
    markdown_block_text = markdown_block_text.strip()
    if markdown_block_text.startswith(
        ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    ):
        return BlockType.HEADING
    elif markdown_block_text.startswith("```") and markdown_block_text.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in markdown_block_text.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith(("- ", "* ")) for line in markdown_block_text.split("\n")):
        return BlockType.UNORDERED_LIST
    if all(
        line.startswith(f"{i}. ")
        for i, line in enumerate(markdown_block_text.split("\n"), start=1)
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown_text: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown_text)
    children: list[HTMLNode] = [block_to_parent_node(block) for block in blocks]
    return ParentNode("div", children)


def block_to_parent_node(markdown_block_text: str) -> ParentNode:
    text: str = markdown_block_text.strip()
    text_parts: list[str] = text.split(maxsplit=1)
    match block_to_block_type(text):
        case BlockType.PARAGRAPH:
            children: list[HTMLNode] = text_to_children_helper(text.replace("\n", " "))
            return ParentNode(BlockType.PARAGRAPH.html_tag, children)
        case BlockType.HEADING:
            children = text_to_children_helper(text)
            return ParentNode(
                f"{BlockType.HEADING.html_tag}{len(text_parts[0])}", children
            )
        case BlockType.CODE:
            stripped = text.removeprefix("```").strip().removesuffix("```")
            children = [text_to_code_child_helper(stripped)]
            return ParentNode(BlockType.CODE.html_tag, children)
        case BlockType.QUOTE:
            children = text_to_children_helper(
                "".join([line.removeprefix("> ") for line in text.split("\n")])
            )
            return ParentNode(BlockType.QUOTE.html_tag, children)
        case BlockType.UNORDERED_LIST:
            children = text_to_unordered_list_children_helper(text)
            return ParentNode(BlockType.UNORDERED_LIST.html_tag, children)
        case BlockType.ORDERED_LIST:
            children = text_to_ordered_list_children_helper(text)
            return ParentNode(BlockType.ORDERED_LIST.html_tag, children)


def text_to_children_helper(stripped_markdown_block_text: str) -> list[HTMLNode]:
    return [
        text_node.textnode_to_htmlnode()
        for text_node in text_to_textnodes(stripped_markdown_block_text)
    ]


def text_to_code_child_helper(stripped_markdown_block_text: str) -> HTMLNode:
    return TextNode(stripped_markdown_block_text, TextType.CODE).textnode_to_htmlnode()


def text_to_unordered_list_children_helper(
    stripped_markdown_block_text: str,
) -> list[HTMLNode]:
    return [
        ParentNode("li", text_to_children_helper(line[2:]))
        for line in stripped_markdown_block_text.split("\n")
    ]


def text_to_ordered_list_children_helper(
    stripped_markdown_block_text: str,
) -> list[HTMLNode]:
    return [
        ParentNode("li", text_to_children_helper(line.split(f"{i}. ")[1]))
        for i, line in enumerate(stripped_markdown_block_text.split("\n"), start=1)
    ]
