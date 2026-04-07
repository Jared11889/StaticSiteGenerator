import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

        matches = extract_markdown_images(
            "I have no images."
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png). Actually, [I LIED!](https://test.org/image1.png) I HAVE MULTIPLE [MUWAHAHAHA](https://test.org/image2.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("I LIED!", "https://test.org/image1.png"), ("MUWAHAHAHA", "https://test.org/image2.png")], matches)

        matches = extract_markdown_links(
            "I have no links."
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )