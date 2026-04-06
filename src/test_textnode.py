import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        nodes_a = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.TEXT),
            TextNode("This is a different text node", TextType.TEXT, "http://www.google.com")
        ]
        nodes_b = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.TEXT),
            TextNode("This is a different text node", TextType.TEXT, "http://www.google.com")
        ]       

        self.assertEqual(nodes_a[0], nodes_b[0])
        self.assertEqual(nodes_a[1], nodes_b[1])
        self.assertEqual(nodes_a[2], nodes_b[2])

    def test_not_eq(self):
        nodes_a = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.TEXT),
            TextNode("This is a different text node", TextType.TEXT, "http://www.google.com")
        ]
        nodes_b = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.TEXT),
            TextNode("This is a different text node", TextType.TEXT, "http://www.google.com")
        ]       

        self.assertNotEqual(nodes_a[0], nodes_b[1])
        self.assertNotEqual(nodes_a[1], nodes_b[2])
        self.assertNotEqual(nodes_a[2], nodes_b[0])

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()