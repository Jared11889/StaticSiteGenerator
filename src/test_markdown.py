import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestMarkdown(unittest.TestCase):
    nodes_bold = [
        TextNode("**This** is markdown.", TextType.TEXT),
        TextNode("This **is** markdown.", TextType.TEXT),
        TextNode("This is markdown.****", TextType.TEXT),
        TextNode("This is **markdown.**", TextType.BOLD)
    ]
    nodes_italic = [
        TextNode("_This_ is markdown.", TextType.TEXT),
        TextNode("This _is_ markdown.", TextType.TEXT),
        TextNode("This is markdown.__", TextType.TEXT)
    ]
    nodes_wrong_code = [
        TextNode("This is `incorrect` `markdown.", TextType.TEXT)
    ]

    def test_split_nodes_delimiter(self):
        nodes_bold = [
            TextNode("**This** is markdown.", TextType.TEXT),
            TextNode("This **is** markdown.", TextType.TEXT),
            TextNode("This is markdown.****", TextType.TEXT),
            TextNode("This is **markdown.**", TextType.BOLD)
        ]   
        nodes_italic = [
            TextNode("_This_ is markdown.", TextType.TEXT),
            TextNode("This _is_ markdown.", TextType.TEXT),
            TextNode("This is markdown.__", TextType.TEXT)
        ]
        nodes_wrong_code = [
            TextNode("This is `incorrect` `markdown.", TextType.TEXT)
        ]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes_wrong_code, "`", TextType.CODE)

        self.assertEqual(
            split_nodes_delimiter(nodes_bold, "**", TextType.BOLD),
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is markdown.", TextType.TEXT),
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.BOLD),
                TextNode(" markdown.", TextType.TEXT),
                TextNode("This is markdown.", TextType.TEXT),
                TextNode("This is **markdown.**", TextType.BOLD)
            ]
        )

        self.assertEqual(
            split_nodes_delimiter(nodes_italic, "_", TextType.ITALIC),
            [
                TextNode("This", TextType.ITALIC),
                TextNode(" is markdown.", TextType.TEXT),
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.ITALIC),
                TextNode(" markdown.", TextType.TEXT),
                TextNode("This is markdown.", TextType.TEXT)
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). Actually, ![I LIED!](https://test.org/image1.png) I HAVE MULTIPLE ![MUWAHAHAHA](https://test.org/image2.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("I LIED!", "https://test.org/image1.png"), ("MUWAHAHAHA", "https://test.org/image2.png")], matches)

        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png). Actually, [I LIED!](https://test.org/image1.png) I HAVE MULTIPLE [MUWAHAHAHA](https://test.org/image2.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("I LIED!", "https://test.org/image1.png"), ("MUWAHAHAHA", "https://test.org/image2.png")], matches)