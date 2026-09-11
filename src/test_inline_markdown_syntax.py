import unittest

from inline_markdown_syntax import *


class TestInlineMarkdownSyntax(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        nodes: list[TextNode] = [
            TextNode("this is normal text", TextType.PLAIN),
            TextNode("this is **bold** text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("italics", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "**", TextType.BOLD),
            [
                TextNode("this is normal text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("italics", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        nodes: list[TextNode] = [
            TextNode("this is normal text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is _italics_ text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "_", TextType.ITALIC),
            [
                TextNode("this is normal text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("italics", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_code(self):
        nodes: list[TextNode] = [
            TextNode("this is normal text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("italics", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is `code` text", TextType.PLAIN),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [
                TextNode("this is normal text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("italics", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_double_code(self):
        nodes: list[TextNode] = [
            TextNode("this is normal text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("italics", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is `code` `text`", TextType.PLAIN),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [
                TextNode("this is normal text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("italics", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
                TextNode("this is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode("text", TextType.CODE),
            ],
        )

    def test_split_nodes_delimiter_raises_outside_delimiter(self):
        nodes: list[TextNode] = [
            TextNode("this is normal text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("italics", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is `code` `text`", TextType.PLAIN),
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "$", TextType.CODE)

    def test_split_nodes_delimiter_raises_invalid_text_nodes(self):
        nodes: list[TextNode] = [
            TextNode("this is normal text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is ", TextType.PLAIN),
            TextNode("italics", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
            TextNode("this is `code `text`", TextType.PLAIN),
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_image(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another link](https://www.example.org)"
        self.assertEqual(
            extract_markdown_link(text),
            [
                ("link", "https://www.example.com"),
                ("another link", "https://www.example.org"),
            ],
        )
