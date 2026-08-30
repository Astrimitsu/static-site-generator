import re
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, text_node_to_html_node
from splitnodes import text_to_textnodes


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


def process_paragraph(block: str) -> ParentNode:
    nodes = text_to_textnodes(block.replace("\n", " "))
    return ParentNode("p", [text_node_to_html_node(node) for node in nodes])


def process_quote_unordered(block: str, md_syntax: str) -> ParentNode:
    nodes = text_to_textnodes(
        " ".join(
            [line.replace(md_syntax, "", 1).lstrip() for line in block.split("\n")]
        )
    )
    return ParentNode("blockquote", [text_node_to_html_node(node) for node in nodes])

def process_code(block:str) -> ParentNode:
    node = LeafNode("code", "\n".join(block.split("\n")[1:-1])+"\n")
    return ParentNode("pre", [node])

def process_ordered_list(block: str) -> ParentNode:
    nodes = [
        text_to_textnodes(line.replace(f"{i}. ", ""))
        for i, line in enumerate(block.split("\n"), 1)
    ]
    return ParentNode("ol", [text_node_to_html_node(line)])


def markdown_to_html_node(markdown: str) -> ParentNode:

    def count_heading_tag(block: str) -> int:
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        return count

    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                children.append(ParentNode("pre", [LeafNode("code", block)]))
            case BlockType.PARAGRAPH:
                children.append(process_paragraph(block))
            case BlockType.QUOTE:
                children.append(process_quote_unordered(block, ">"))
            case BlockType.UNORDERED_LIST:
                children.append(process_quote_unordered(block, "- "))
            case BlockType.ORDERED_LIST:
                children.append(process_ordered_list(block))
