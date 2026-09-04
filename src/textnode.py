from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: None | str = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: None | str = url

    def __eq__(self, other: object):
        if not isinstance(other, TextNode):
            return NotImplemented
        return vars(self) == vars(other)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    requires_url = (TextType.LINK, TextType.IMAGE)
    if text_node.text_type in requires_url and text_node.url is None:
        raise ValueError(f"Error: {text_node!r} missing parameter: URL")

    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK if text_node.url is not None:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE if text_node.url is not None:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(
        f"Error: {text_node!r}: {text_node.text_type} is not a valid Text Type"
    )
