import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def leaf_node_possitive(self):
        leaf_node: LeafNode = LeafNode("p", "Hey there", {"href": "www.google.net"})
        self.assertEqual(leaf_node.tag, "p")
        self.assertEqual(leaf_node.value, "Hey there")
        self.assertEqual(leaf_node.props, {"href": "www.google.net"})

    def leaf_node_negative(self):
        leaf_node: LeafNode = LeafNode("p", "Hey there", {"href": "www.google.net"})
        self.assertEqual(leaf_node.tag, "p")
        self.assertIsNone(leaf_node.value)
        self.assertIsNone(leaf_node.props)

    def test_to_html(self):
        leaf_node: LeafNode = LeafNode("p", "Hey there", {"href": "www.google.net"})
        self.assertEqual(leaf_node.to_html(), '<p href="www.google.net">Hey there</p>')

    def test_to_html_no_value(self):
        leaf_node: LeafNode = LeafNode("p", "", {"href": "www.google.net"})
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_no_tag(self):
        leaf_node: LeafNode = LeafNode("", "Hello world", {"href": "www.google.net"})
        self.assertEqual(leaf_node.to_html(), "Hello world")

    def test_repr(self):
        leaf_node: LeafNode = LeafNode("p", "Hey there", {"href": "www.google.net"})
        self.assertEqual(
            leaf_node.__repr__(),
            "HTMLNode(tag = p, value = Hey there,  props = {'href': 'www.google.net'})",
        )
