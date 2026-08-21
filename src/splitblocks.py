import re

from enum import Enum

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "block code"
    quote = "quote"
    bullet_list = "bullet list"
    numbered_list = "ordered list"

def block_to_block_type(block: str) -> BlockType:
    regex_header = r"^#{1,6} .+"

    if re.match(regex_header, block):
        return BlockType.heading

def markdown_to_blocks(markdown: str) -> list[str]:
    return [
        stripped_block
        for stripped_block in [block.strip() for block in markdown.split("\n\n")]
        if stripped_block
    ]
