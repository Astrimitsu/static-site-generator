import re
from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode
from splitnodes import text_to_textnodes
from textnode import text_node_to_html_node


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


def count_heading_tag(block: str) -> int:
    count = 0
    for char in block:
        if char != "#":
            break
        count += 1
    return count


def process_heading(block: str) -> ParentNode:
    heading_count = count_heading_tag(block)
    nodes = text_to_textnodes(block.removeprefix(f"{'#' * heading_count} "))
    return ParentNode(
        f"h{heading_count}", [text_node_to_html_node(node) for node in nodes]
    )


def process_quote(block: str) -> ParentNode:
    nodes = text_to_textnodes(
        " ".join([line.removeprefix(">").lstrip() for line in block.split("\n")])
    )
    return ParentNode("blockquote", [text_node_to_html_node(node) for node in nodes])


def process_code(block: str) -> ParentNode:
    node = LeafNode("code", "\n".join(block.split("\n")[1:-1]) + "\n")
    return ParentNode("pre", [node])


def process_unordered_list(block: str) -> ParentNode:
    nodes = [text_to_textnodes(line.removeprefix("- ")) for line in block.split("\n")]
    return ParentNode(
        "ul",
        [
            ParentNode("li", [text_node_to_html_node(leaf) for leaf in parent])
            for parent in nodes
        ],
    )


def process_ordered_list(block: str) -> ParentNode:
    nodes = [
        text_to_textnodes(line.removeprefix(f"{i}. "))
        for i, line in enumerate(block.split("\n"), 1)
    ]
    return ParentNode(
        "ol",
        [
            ParentNode("li", [text_node_to_html_node(leaf) for leaf in parent])
            for parent in nodes
        ],
    )


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(process_paragraph(block))
            case BlockType.HEADING:
                children.append(process_heading(block))
            case BlockType.CODE:
                children.append(process_code(block))
            case BlockType.QUOTE:
                children.append(process_quote(block))
            case BlockType.UNORDERED_LIST:
                children.append(process_unordered_list(block))
            case BlockType.ORDERED_LIST:
                children.append(process_ordered_list(block))
            case _:
                raise ValueError(f"Invalid BlockType: {block_type} (Something very bad happened if you see this.)")
    return ParentNode("div", children)
