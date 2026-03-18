import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # def setUp(self):
    #     self.node_italic_a = TextNode("This is a text node", TextType.ITALIC)
    #     self.node_plain_a = TextNode("This is a text node", TextType.PLAIN)
    #     self.node_bold_a = TextNode("This is a text node", TextType.BOLD)
    #     self.node_code_a = TextNode("This is a text node", TextType.CODE)
    #     self.node_link_a = TextNode("This is a text node", TextType.LINK)
    #     self.node_image_a = TextNode("This is a text node", TextType.IMAGE)
    #     self.node_italic_b = TextNode("This is a text node", TextType.ITALIC)
    #     self.node_plain_b = TextNode("This is a text node", TextType.PLAIN)
    #     self.node_bold_b = TextNode("This is a text node", TextType.BOLD)
    #     self.node_code_b = TextNode("This is a text node", TextType.CODE)
    #     self.node_link_b = TextNode("This is a text node", TextType.LINK)
    #     self.node_image_b = TextNode("This is a text node", TextType.IMAGE)
    #     self.node_italic_url = TextNode("This is a different text node", TextType.ITALIC, "http://www.google.com")
    #     self.node_plain_url = TextNode("This is a different text node", TextType.PLAIN, "http://www.google.com")
    #     self.node_bold_url = TextNode("This is a different text node", TextType.BOLD, "http://www.google.com")
    #     self.node_code_url = TextNode("This is a different text node", TextType.CODE, "http://www.google.com")
    #     self.node_link_url = TextNode("This is a different text node", TextType.LINK, "http://www.google.com")
    #     self.node_image_url = TextNode("This is a different text node", TextType.IMAGE, "http://www.google.com")

    def test_eq(self):
        nodes_a = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.PLAIN),
            TextNode("This is a different text node", TextType.PLAIN, "http://www.google.com")
        ]
        nodes_b = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.PLAIN),
            TextNode("This is a different text node", TextType.PLAIN, "http://www.google.com")
        ]       

        self.assertEqual(nodes_a[0], nodes_b[0])
        self.assertEqual(nodes_a[1], nodes_b[1])
        self.assertEqual(nodes_a[2], nodes_b[2])

    def test_not_eq(self):
        nodes_a = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.PLAIN),
            TextNode("This is a different text node", TextType.PLAIN, "http://www.google.com")
        ]
        nodes_b = [
            TextNode("This is a text node", TextType.ITALIC),
            TextNode("This is a text node", TextType.PLAIN),
            TextNode("This is a different text node", TextType.PLAIN, "http://www.google.com")
        ]       

        self.assertNotEqual(nodes_a[0], nodes_b[1])
        self.assertNotEqual(nodes_a[1], nodes_b[2])
        self.assertNotEqual(nodes_a[2], nodes_b[0])

if __name__ == "__main__":
    unittest.main()