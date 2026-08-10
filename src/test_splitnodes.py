import unittest

from splitnodes import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def setUp(self) -> None:
        self.textnode_bold_one_instance = TextNode(
            "this is __bold__ text", TextType.BOLD_TEXT
        )
        self.textnode_italic_one_instance = TextNode(
            "this is *italic* text", TextType.ITALIC_TEXT
        )
        self.textnode_bold_two_instances = TextNode(
            "this is __bold__ text __with two instances__", TextType.BOLD_TEXT
        )
        self.textnode_missing_terminator = TextNode(
            "this is a `malformed code block", TextType.CODE_TEXT
        )
        self.textnode_starting_as_bold = TextNode(
            "__bold text__ immediately", TextType.BOLD_TEXT
        )
        self.textnode_missing_terminator_one_instance = TextNode(
            "this is a `code block` with `one missing terminator", TextType.CODE_TEXT
        )
        self.textnode_plaintext = TextNode("hello i am plain text", TextType.PLAIN_TEXT)

    def test_split_node_delimiter(self):
        self.assertEqual(
            split_nodes_delimiter(
                [self.textnode_bold_one_instance], "__", TextType.BOLD_TEXT
            ),
            [
                TextNode("this is ", TextType.PLAIN_TEXT, None),
                TextNode("bold", TextType.BOLD_TEXT, None),
                TextNode(" text", TextType.PLAIN_TEXT, None),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter(
                [self.textnode_italic_one_instance], "*", TextType.ITALIC_TEXT
            ),
            [
                TextNode("this is ", TextType.PLAIN_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
                TextNode(" text", TextType.PLAIN_TEXT, None),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter(
                [self.textnode_bold_two_instances], "__", TextType.BOLD_TEXT
            ),
            [
                TextNode("this is ", TextType.PLAIN_TEXT, None),
                TextNode("bold", TextType.BOLD_TEXT, None),
                TextNode(" text ", TextType.PLAIN_TEXT, None),
                TextNode("with two instances", TextType.BOLD_TEXT, None),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter(
                [self.textnode_plaintext, self.textnode_italic_one_instance],
                "*",
                TextType.ITALIC_TEXT,
            ),
            [
                TextNode("hello i am plain text", TextType.PLAIN_TEXT, None),
                TextNode("this is ", TextType.PLAIN_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
                TextNode(" text", TextType.PLAIN_TEXT, None),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter(
                [self.textnode_starting_as_bold], "__", TextType.BOLD_TEXT
            ),
            [
                TextNode("bold text", TextType.BOLD_TEXT),
                TextNode(" immediately", TextType.PLAIN_TEXT),
            ],
        )
        self.assertRaises(
            ValueError,
            split_nodes_delimiter,
            [self.textnode_missing_terminator],
            "`",
            TextType.CODE_TEXT,
        )
        self.assertRaises(
            ValueError,
            split_nodes_delimiter,
            [self.textnode_missing_terminator_one_instance],
            "`",
            TextType.CODE_TEXT,
        )


class TestExtractImageLink(unittest.TestCase):
    def setUp(self) -> None:
        self.text1 = (
            "ahhhh this is test text test test and testing that __bold text and__ ![some link alt text here](fobs.png) wwaoooh foxes are orange"
            "[linkerino here for realsies](http://coollinknotvirus.ru)"
        )
        self.text2 = (
            "![foxpicture1](foxpicture1.png)![foxpicture2](foxpicture2.png)![foxpicture3](foxpicture3.png)"
            "[foxlink1](http://fox.com/foxlink1)[foxlink2](http://fox.com/foxlink2)[foxlink3](http://fox.com/foxlink3)"
        )

    def test_extract_image_link(self):
        self.assertEqual(
            extract_markdown_links(self.text1),
            [("linkerino here for realsies", "http://coollinknotvirus.ru")],
        )
        self.assertEqual(
            extract_markdown_images(self.text1),
            [("some link alt text here", "fobs.png")],
        )
        self.assertEqual(
            extract_markdown_images(self.text2),
            [
                ("foxpicture1", "foxpicture1.png"),
                ("foxpicture2", "foxpicture2.png"),
                ("foxpicture3", "foxpicture3.png"),
            ],
        )
        self.assertEqual(
            extract_markdown_links(self.text2),
            [
                ("foxlink1", "http://fox.com/foxlink1"),
                ("foxlink2", "http://fox.com/foxlink2"),
                ("foxlink3", "http://fox.com/foxlink3"),
            ],
        )