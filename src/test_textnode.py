import unittest

from src.leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        first_node: TextNode = TextNode("This is a test node", TextType.BOLD)
        second_node: TextNode = TextNode("This is a test node", TextType.BOLD)

        self.assertEqual(first_node, second_node)

    def test_eq_negative_text(self):
        first_node: TextNode = TextNode("This is a test node,", TextType.BOLD)
        second_node: TextNode = TextNode("This is a test node", TextType.BOLD)
        self.assertNotEqual(first_node, second_node)

    def test_eq_negative_url(self):
        first_node: TextNode = TextNode(
            "This is a test node", TextType.BOLD, "link.https:"
        )
        second_node: TextNode = TextNode(
            "This is a test node", TextType.BOLD, "linklink.https:"
        )
        self.assertNotEqual(first_node, second_node)

    def test_eq_postive_url(self):
        first_node: TextNode = TextNode(
            "This is a test node", TextType.BOLD, "link.https:"
        )
        second_node: TextNode = TextNode(
            "This is a test node", TextType.BOLD, "link.https:"
        )
        self.assertEqual(first_node, second_node)

    def test_textnode_to_htmlnode_plain_text(self):
        node: TextNode = TextNode("This is a text node", TextType.PLAIN)
        leaf_node: LeafNode = node.textnode_to_htmlnode()
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "This is a text node")

    def test_textnode_to_htmlnode_bold_text(self):
        node: TextNode = TextNode("This is a bold text node", TextType.BOLD)
        leaf_node: LeafNode = node.textnode_to_htmlnode()
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "This is a bold text node")

    def test_textnode_to_htmlnode_code_text(self):
        node: TextNode = TextNode("This is a code text node", TextType.CODE)
        leaf_node: LeafNode = node.textnode_to_htmlnode()
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "This is a code text node")

    def test_textnode_to_htmlnode_image_link(self):
        node: TextNode = TextNode(
            "This is an image link text node",
            TextType.IMAGE_LINK,
            "https://example.com",
        )
        leaf_node: LeafNode = node.textnode_to_htmlnode()
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "This is an image link text node")

    def test_textnode_to_htmlnode_link(self):
        node: TextNode = TextNode(
            "This is a link text node", TextType.LINK, "https://example.com"
        )
        leaf_node: LeafNode = node.textnode_to_htmlnode()
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "This is a link text node")

    def test_textnode_to_htmlnode_link_no_url(self):
        node: TextNode = TextNode("This is a link text node", TextType.LINK)
        with self.assertRaises(ValueError):
            node.textnode_to_htmlnode()

    def test_textnode_to_htmlnode_image_link_no_url(self):
        node: TextNode = TextNode(
            "This is an image link text node", TextType.IMAGE_LINK
        )
        with self.assertRaises(ValueError):
            node.textnode_to_htmlnode()


if __name__ == "__main__":
    _ = unittest.main()
