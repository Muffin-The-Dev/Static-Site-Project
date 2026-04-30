from enum import Enum



def markdown_to_block(text):
    split_text = text.split("\n\n")
    filtered = []
    for to_filter_text in split_text:
        check_text = to_filter_text.strip()
        if check_text != "":
            filtered.append(check_text)
    return filtered

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(text):
    multiline_check = text.split("\n")
    if text.startswith(("# ", "## ", "### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    elif text.startswith(("```\n"))and text.endswith(("```")):
        return BlockType.CODE
    elif all(line.startswith(">")for line in multiline_check):
        return BlockType.QUOTE
    elif all(line.startswith("- ")for line in multiline_check):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i+1}. ")for i,line in enumerate(multiline_check)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

    
