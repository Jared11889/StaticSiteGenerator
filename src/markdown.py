import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT: #ensure that node is plain text
            new_nodes.append(old_node)
            continue
        
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0: #check for unclosed tags
            raise ValueError("Unclosed markdown tag present")

        for index, node in enumerate(split_text):
            if node == "":
                continue

            if index % 2 == 0:
                new_nodes.append(TextNode(node, TextType.TEXT))
            else:
                new_nodes.append(TextNode(node, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"(?:!\[)(.*?)(?:\])(?:\()(.*?)(?:\))", text)

def extract_markdown_links(text):
    return re.findall(r"(?:\[)(.*?)(?:\])(?:\()(.*?)(?:\))", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT: #ensure that node is plain text
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text) 
        if not images: #check for images, only proceed if there are any.
            new_nodes.append(old_node)
            continue

        nodes_to_insert = []
        text_queue = old_node.text
        for image in images:
            split = text_queue.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if split[0] != "":
                nodes_to_insert.append(TextNode(split[0], TextType.TEXT))
            nodes_to_insert.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text_queue = split[-1]
        
        if text_queue != "":
            nodes_to_insert.append(TextNode(text_queue, TextType.TEXT))
        new_nodes.extend(nodes_to_insert)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT: #ensure that node is plain text
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links: #check for links, only proceed if there are any.
            new_nodes.append(old_node)
            continue

        nodes_to_insert = []
        text_queue = old_node.text
        for link in links:
            split = text_queue.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if split[0] != "":
                nodes_to_insert.append(TextNode(split[0], TextType.TEXT))
            nodes_to_insert.append(TextNode(link[0], TextType.LINK, link[1]))
            text_queue = split[-1]
        
        if text_queue != "":
            nodes_to_insert.append(TextNode(text_queue, TextType.TEXT))
        new_nodes.extend(nodes_to_insert)

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        block = block.strip()

        if block == "":
            continue

        blocks.append(block)

    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```\n[\s\S]*```$", block):
        return BlockType.CODE
    elif re.match(r"^>.*(\n>.*)*$", block):
        return BlockType.QUOTE
    elif re.match(r"^- .*(\n- .*)*$", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^1\. ", block):
        lines = block.split("\n")
        for index, line in enumerate(lines, start=1):
            if not re.match(rf"^{index}\. ", line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH