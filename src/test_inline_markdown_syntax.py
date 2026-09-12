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

    def test_split_nodes_image(self):
        nodes: list[TextNode] = [
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
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.PLAIN,
            ),
        ]

        self.assertEqual(
            split_nodes_image(nodes),
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
                TextNode(
                    "This is text with an ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "image", TextType.IMAGE_LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
        )

    def test_split_nodes_image_multiple_images(self):
        nodes: list[TextNode] = [
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
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.PLAIN,
            ),
        ]

        self.assertEqual(
            split_nodes_image(nodes),
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
                TextNode(
                    "This is text with an ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "image", TextType.IMAGE_LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(
                    " and another ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "second image",
                    TextType.IMAGE_LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
        )

    def test_split_nodes_link(self):
        nodes: list[TextNode] = [
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
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev)",
                TextType.PLAIN,
            ),
        ]

        self.assertEqual(
            split_nodes_link(nodes),
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
                TextNode(
                    "This is text with a link ",
                    TextType.PLAIN,
                ),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
        )

    def test_split_nodes_link_multiple_links(self):
        nodes: list[TextNode] = [
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
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.PLAIN,
            ),
        ]
        self.assertEqual(
            split_nodes_link(nodes),
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
                TextNode(
                    "This is text with a link ",
                    TextType.PLAIN,
                ),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_nodes_link_empty_or_spaced(self):
        nodes: list[TextNode] = [
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
            TextNode("", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode(
                "This is text with a link   [to boot dev](https://www.boot.dev) and   [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.PLAIN,
            ),
        ]

        self.assertEqual(
            split_nodes_link(nodes),
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
                TextNode(
                    "This is text with a link   ",
                    TextType.PLAIN,
                ),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and   ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_nodes_images_empty_or_spaced(self):
        nodes: list[TextNode] = [
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
            TextNode("", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode(
                "This is text with an   ![image](https://i.imgur.com/zjjcJKZ.png) and another   ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.PLAIN,
            ),
        ]
        self.assertEqual(
            split_nodes_image(nodes),
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
                TextNode(
                    "This is text with an   ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "image", TextType.IMAGE_LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(
                    " and another   ",
                    TextType.PLAIN,
                ),
                TextNode(
                    "second image",
                    TextType.IMAGE_LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
        )
