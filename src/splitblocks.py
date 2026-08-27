import re
from enum import Enum
from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "block code"
    QUOTE = "quote"
    UNORDERED_LIST = "bullet list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(block: str) -> BlockType:
    if not block:
        return BlockType.PARAGRAPH

    regex_header = r"^#{1,6} .+"
    split_block = block.splitlines()

    def lines_start_with(markdown: str) -> bool:
        return all(line.startswith(markdown) for line in split_block)

    if re.match(regex_header, block):
        return BlockType.HEADING
    if split_block[0] == "```" and split_block[-1] == "```" and len(split_block) >= 3:
        return BlockType.CODE
    if lines_start_with(">"):
        return BlockType.QUOTE
    if lines_start_with("- "):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(split_block, 1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [
        stripped_block
        for stripped_block in [block.strip() for block in markdown.split("\n\n")]
        if stripped_block
    ]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    parent_node = HTMLNode()
    parent_node.children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
