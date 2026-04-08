import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]

        text2 = "Welcome to the **Project Alpha** test. We are currently in the _beta phase_ of development. Please review the `config.py` file before proceeding. You can find the documentation at this [helpful link](https://example.com/docs). Here is a preview of the UI: ![UI Screenshot](https://example.com/logo.png)"
        nodes2 = [
            TextNode("Welcome to the ", TextType.TEXT),
            TextNode("Project Alpha", TextType.BOLD),
            TextNode(" test. We are currently in the ", TextType.TEXT),
            TextNode("beta phase", TextType.ITALIC),
            TextNode(" of development. Please review the ", TextType.TEXT),
            TextNode("config.py", TextType.CODE),
            TextNode(" file before proceeding. You can find the documentation at this ", TextType.TEXT),
            TextNode("helpful link", TextType.LINK, "https://example.com/docs"),
            TextNode(". Here is a preview of the UI: ", TextType.TEXT),
            TextNode("UI Screenshot", TextType.IMAGE, "https://example.com/logo.png")
        ]

        text3 = "The **first** word and the **last** word are bold. An _italic_ word here and another _italic_ word there. The `print()` function and the `import` statement are code."
        nodes3 = [
            TextNode("The ", TextType.TEXT),
            TextNode("first", TextType.BOLD),
            TextNode(" word and the ", TextType.TEXT),
            TextNode("last", TextType.BOLD),
            TextNode(" word are bold. An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word here and another ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word there. The ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" function and the ", TextType.TEXT),
            TextNode("import", TextType.CODE),
            TextNode(" statement are code.", TextType.TEXT)
        ]

        self.assertListEqual(text_to_textnodes(text), nodes)
        self.assertListEqual(text_to_textnodes(text2), nodes2)
        self.assertListEqual(text_to_textnodes(text3), nodes3)

