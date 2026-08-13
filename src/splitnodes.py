import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    input_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    processed_nodes: list[TextNode] = []
    for node in input_nodes:
        if node.text_type is TextType.PLAIN_TEXT:
            processed_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError(
                f"Error: Text {node.text} missing expected terminator {delimiter}"
            )
        for i, split_text in enumerate(split_node):
            if split_text:
                if i % 2 == 0:
                    processed_nodes.append(TextNode(split_text, TextType.PLAIN_TEXT))
                if i % 2 == 1:
                    processed_nodes.append(TextNode(split_text, text_type))
    return processed_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(input_nodes: list[TextNode]) -> list[TextNode]:
    processed_nodes: list[TextNode] = []
    for node in input_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            processed_nodes.append(node)
            continue
        for image in images:
            

    return processed_nodes