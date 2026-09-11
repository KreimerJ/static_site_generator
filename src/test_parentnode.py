import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode(
            "div", [child_node], {"href": "https://www.google.com"}
        )

        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.google.com"><span><b>grandchild</b></span></div>',
        )

    def test_error_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("", [child_node], {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_error_no_children(self):
        parent_node = ParentNode("div", "", {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            parent_node.to_html()
