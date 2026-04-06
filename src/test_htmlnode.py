import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_data_members(self):
        childnode = HTMLNode(value="I'm a child")
        node = HTMLNode(tag="b", value="I'm bold", children=childnode, props={"href": "google.com"})
        emptynode = HTMLNode()

        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "I'm bold")
        self.assertEqual(node.children, childnode)
        self.assertEqual(node.props, {"href": "google.com"})
        self.assertEqual(emptynode.tag, None)
        self.assertEqual(emptynode.value, None)
        self.assertEqual(emptynode.children, None)
        self.assertEqual(emptynode.props, None)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "google.com", "target": "_blank"})
        emptynode = HTMLNode()

        self.assertEqual(emptynode.props_to_html(), "")
        self.assertEqual(node.props_to_html(), " href=\"google.com\" target=\"_blank\"")

    def test_repr(self):
        node = HTMLNode(tag="b", value="I'm bold", children=None, props={"href": "google.com"})

        self.assertEqual(node.__repr__(), f"{node.tag}, {node.value}, {node.children}, {node.props}")

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_repr(self):
        node = LeafNode("a", "I have an anchor tag!", props={"href": "google.com"})
        self.assertEqual(node.__repr__(), f"{node.tag}, {node.value}, {node.props}")

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