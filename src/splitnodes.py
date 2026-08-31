import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    input_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    processed_nodes: list[TextNode] = []
    for node in input_nodes:
        if node.text_type is not TextType.PLAIN_TEXT:
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
        if node.text_type is not TextType.PLAIN_TEXT:
            processed_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            processed_nodes.append(node)
            continue

        text = node.text
        rest = ""
        for image in images:
            alt, url = image
            current, rest = text.split(f"![{alt}]({url})", 1)
            if current:
                processed_nodes.append(TextNode(current, TextType.PLAIN_TEXT))
            processed_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = rest
        if rest:
            processed_nodes.append(TextNode(rest, TextType.PLAIN_TEXT))

    return processed_nodes


def split_nodes_link(input_nodes: list[TextNode]) -> list[TextNode]:
    processed_nodes: list[TextNode] = []
    for node in input_nodes:
        if node.text_type is not TextType.PLAIN_TEXT:
            processed_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            processed_nodes.append(node)
            continue

        text = node.text
        rest = ""
        for link in links:
            link_text, url = link
            current, rest = text.split(f"[{link_text}]({url})", 1)
            if current:
                processed_nodes.append(TextNode(current, TextType.PLAIN_TEXT))
            processed_nodes.append(TextNode(link_text, TextType.LINK, url))
            text = rest
        if rest:
            processed_nodes.append(TextNode(rest, TextType.PLAIN_TEXT))

    return processed_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    delimiters = [
        ("**", TextType.BOLD_TEXT),
        ("_", TextType.ITALIC_TEXT),
        ("`", TextType.CODE_TEXT),
    ]
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
