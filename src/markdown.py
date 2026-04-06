from textnode import TextNode, TextType

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