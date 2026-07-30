from enum import Enum


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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
