import re

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "block code"
    QUOTE = "quote"
    UNORDERED_LIST = "bullet list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(block: str) -> BlockType:
    regex_header = r"^#{1,6} .+"
    split_block = block.splitlines()

    def lines_startswith(markdown: str) -> bool:
        return all(line.startswith(markdown) for line in split_block)

    if re.match(regex_header, block):
        return BlockType.HEADING
    if split_block[0].startswith("```") and split_block[-1].endswith("```") and len(split_block) >= 3:
        return BlockType.CODE
    if block.startswith(">") and lines_startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- ") and lines_startswith("- "):
        return BlockType.UNORDERED_LIST
    if block[:3] == "1. ":
        list_number = 2
        is_numbered_list = True
        for line in split_block[1:]:
            if not line.startswith(f"{list_number}. "):
                is_numbered_list = False
                break
            list_number += 1
        if is_numbered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [
        stripped_block
        for stripped_block in [block.strip() for block in markdown.split("\n\n")]
        if stripped_block
    ]
