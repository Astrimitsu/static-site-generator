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

    def count_heading_tag(block: str) -> int:
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        return count

    def get_html_tag_from_blocktype(blocktype: BlockType) -> str:
        match block_type:
            case BlockType.PARAGRAPH:
                return "p"
            case BlockType.HEADING:
                return f"h{count_heading_tag(block)}"
            case BlockType.CODE:
                return "pre "
            case BlockType.QUOTE:
                return "blockquote"
            case BlockType.UNORDERED_LIST:
                return "ul"
            case BlockType.ORDERED_LIST:
                return "ol"
            case _:
                raise ValueError(f"Invalid Block type: {repr(blocktype)}")

    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        tag = get_html_tag_from_blocktype(block_type)
        if BlockType is BlockType.CODE:
            children.append(HTMLNode(tag, None, [HTMLNode("code", block)]))
        else:
