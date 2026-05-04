def extract_title(markdown):
    split_markdown = markdown.split("\n")
    rejoin_list = []
    for line in split_markdown:
        if line.startswith("# "):
            line = line[2:]
            line = line.strip()
            return line
    raise Exception