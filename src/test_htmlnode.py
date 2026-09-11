import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htlmnode_none(self):
        node: HTMLNode = HTMLNode()
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertIsNone(node.tag)

    def test_htmlnode_possitive(self):
        first_child_node: HTMLNode = HTMLNode()
        second_child_node: HTMLNode = HTMLNode()
        node: HTMLNode = HTMLNode(
            "p",
            "this is a parragraph",
            [first_child_node, second_child_node],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "this is a parragraph")
        self.assertEqual(node.children, [first_child_node, second_child_node])
        self.assertEqual(
            node.props,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

    def test_to_html_none(self):
        node: HTMLNode = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_possitve(self):
        first_child_node: HTMLNode = HTMLNode()
        second_child_node: HTMLNode = HTMLNode()
        node: HTMLNode = HTMLNode(
            "p",
            "this is a parragraph",
            [first_child_node, second_child_node],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
