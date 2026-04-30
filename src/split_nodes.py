from textnode import TextNode, TextType
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes,delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node = old_node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("invalid markdown syntax")
        else:
            for i in range(len(split_node)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_node[i],TextType.TEXT))
                else:
                   new_nodes.append(TextNode(split_node[i],text_type))
    return new_nodes
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        if len(images) == 0:
            new_nodes.append(old_node)
        else:
            for image in images:
                split_text = f"![{image[0]}]({image[1]})"
                image_text = remaining_text.split(split_text, 1)
                if image_text[0] != "":
                    new_nodes.append(TextNode(image_text[0],TextType.TEXT))
                new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
                remaining_text = image_text[1]
                if remaining_text!= "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        if len(links) == 0:
            new_nodes.append(old_node)
        else:
            for link in links:
                split_text = f"[{link[0]}]({link[1]})"
                link_text = remaining_text.split(split_text, 1)
                if link_text[0] != "":
                    new_nodes.append(TextNode(link_text[0],TextType.TEXT))
                new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
                remaining_text = link_text[1]
                if remaining_text!= "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
