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
    regex_code_start = r"^`{3}(?!`)"
    split_block = block.splitlines()

    def lines_startswith(markdown: str) -> bool:
        return all(line.startswith(markdown) for line in split_block)

    if re.match(regex_header, block):
        return BlockType.HEADING
    if (
        re.match(regex_code_start, split_block[0])
        and split_block[-1] == "```"
        and len(split_block) >= 3
    ):
        return BlockType.CODE
    if block.startswith(">") and lines_startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- ") and lines_startswith("- "):
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        list_number = 0
        is_numbered_list = all(
            line.startswith(f"{(list_number := list_number + 1)}. ")
            for line in split_block
        )
        if is_numbered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [
        stripped_block
        for stripped_block in [block.strip() for block in markdown.split("\n\n")]
        if stripped_block
    ]
