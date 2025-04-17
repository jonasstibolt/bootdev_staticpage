from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    def __repr__(self):
        return self.value
    
def block_to_block_type(block):
    lines = block.splitlines()
    index = 0
    if not block.strip():
         raise Exception("invalid markdown format")
    if block.startswith(("# ", "## ", "###", "#### ", "##### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.strip().startswith(">") for line in lines):
            return BlockType.QUOTE
    if all(line.strip().startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
    for line in lines:
        index += 1
        if line.startswith(f"{index}. "):
            return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
     pass