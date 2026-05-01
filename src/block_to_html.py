from markdown_to_block import markdown_to_block, block_to_block_type,BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_textnodes import text_to_textnodes,TextNode,TextType
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        else:
            raise ValueError("invalid block type")
        children.append(node)
    return ParentNode("div", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0 
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    stripped = block[4:-3]
    text_node = TextNode(stripped, TextType.TEXT)
    html_text_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_text_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        if not line.startswith("-"):
            raise ValueError("invalid list format")
        stripped = line[2:]
        children.append(ParentNode("li", text_to_children(stripped)))
    return ParentNode("ul", children)
    
def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        if not line.startswith(prefix):
            raise ValueError("invalid ordered list")
        stripped = line[len(prefix):]
        children.append(ParentNode("li", text_to_children(stripped)))
    return ParentNode("ol", children)
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children =[]
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children