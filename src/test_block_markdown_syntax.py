import unittest
from textwrap import dedent

from block_markdown_syntax import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_block_with_trailing_whitespace(self):
        md = dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_block_with_more_spaces(self):
        md = dedent("""
               This is **bolded** paragraph



               This is another paragraph with _italic_ text and `code` here
               This is the same paragraph on a new line



               - This is a list
               - with items
               """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_markdown_syntax_heading(self):
        text: str = dedent("""# Heading 1
                   """)
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_markdown_syntax_code(self):
        text: str = dedent("""
            ```
            This is a code block
            with some code inside
            ```
            """)
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_block_markdown_syntax_quote(self):
        text: str = dedent("""
            > This is a quote block.
            > Every line starts with a greater than character.
            """)
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_markdown_syntax_unordered_list(self):
        text: str = dedent("""
            - Unordered item 1
            - Unordered item 2
            - Unordered item 3
            """)
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_markdown_syntax_ordered_list(self):
        text: str = dedent("""
            1. First ordered item
            2. Second ordered item
            3. Third ordered item
            """)
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_block_markdown_syntax_parragraph(self):
        text: str = dedent("""
            This is a paragraph of text. It can span multiple lines
            and continues here as regular text.
            """)
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
