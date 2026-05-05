import os
from extracttitle import extract_title
from block_to_html import markdown_to_html_node
from htmlnode import ParentNode,LeafNode,HTMLNode

def generate_page(from_path, template_path,dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        contents = f.read()
    with open(template_path) as g:
        template_contents = g.read()
    node_to_html = markdown_to_html_node(contents)
    html_string = node_to_html.to_html()
    title = extract_title(contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_string)
    template_contents = template_contents.replace('href="/',f'href="{basepath}')
    template_contents = template_contents.replace('src="/',f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as w:
       w.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path.replace(".md",".html")
                generate_page(from_path,template_path,dest_path,basepath)
        else:
            generate_pages_recursive(from_path,template_path,dest_path,basepath)