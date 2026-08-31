import unittest

from splitnodes import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def setUp(self) -> None:
        self.textnode_bold_one_instance = TextNode(
            "this is __bold__ text", TextType.PLAIN_TEXT
        )
        self.textnode_italic_one_instance = TextNode(
            "this is *italic* text", TextType.PLAIN_TEXT
        )
        self.textnode_bold_two_instances = TextNode(
            "this is __bold__ text __with two instances__", TextType.PLAIN_TEXT
        )
        self.textnode_missing_terminator = TextNode(
            "this is a `malformed code block", TextType.PLAIN_TEXT
        )
        self.textnode_starting_as_bold = TextNode(
            "__bold text__ immediately", TextType.PLAIN_TEXT
        )
        self.textnode_missing_terminator_one_instance = TextNode(
            "this is a `code block` with `one missing terminator", TextType.PLAIN_TEXT
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


class TestExtractImageLinkTestItems(unittest.TestCase):

    def setUp(self) -> None:
        self.text1 = (
            "ahhhh this is test text test test and testing that __bold text and__ ![some link alt text here](fobs.png) wwaoooh foxes are orange"
            "[linkerino here for realsies](http://coollinknotvirus.ru)"
        )
        self.text2 = (
            "![foxpicture1](foxpicture1.png)![foxpicture2](foxpicture2.png)![foxpicture3](foxpicture3.png)"
            "[foxlink1](http://fox.com/foxlink1)[foxlink2](http://fox.com/foxlink2)[foxlink3](http://fox.com/foxlink3)"
        )


class TestExtractImage(TestExtractImageLinkTestItems):

    def test_extract_image(self):
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


class TestExtractLink(TestExtractImageLinkTestItems):
    def test_extract_link(self):
        self.assertEqual(
            extract_markdown_links(self.text1),
            [("linkerino here for realsies", "http://coollinknotvirus.ru")],
        )

        self.assertEqual(
            extract_markdown_links(self.text2),
            [
                ("foxlink1", "http://fox.com/foxlink1"),
                ("foxlink2", "http://fox.com/foxlink2"),
                ("foxlink3", "http://fox.com/foxlink3"),
            ],
        )


class TestSplitNodeImagesLinksTestItems(unittest.TestCase):
    def setUp(self) -> None:
        self.two_images = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.PLAIN_TEXT,
            )
        ]
        self.two_links = [
            TextNode(
                "This is text with [two links](http://foxpetters.org) and including a new [second link](http://foxpetters2.org)",
                TextType.PLAIN_TEXT,
            )
        ]
        self.link_and_image = [
            TextNode(
                "This is some text with ![an image](fox.png), but also includes [a standard link](http://foxpetters.org)",
                TextType.PLAIN_TEXT,
            )
        ]


class TestSplitNodeImages(TestSplitNodeImagesLinksTestItems):
    def test_split_images(self):
        self.assertListEqual(
            split_nodes_image(self.two_images),
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )
        self.assertListEqual(
            split_nodes_image(self.two_links),
            [
                TextNode(
                    "This is text with [two links](http://foxpetters.org) and including a new [second link](http://foxpetters2.org)",
                    TextType.PLAIN_TEXT,
                    None,
                )
            ],
        )
        self.assertListEqual(
            split_nodes_image(self.link_and_image),
            [
                TextNode("This is some text with ", TextType.PLAIN_TEXT, None),
                TextNode("an image", TextType.IMAGE, "fox.png"),
                TextNode(
                    ", but also includes [a standard link](http://foxpetters.org)",
                    TextType.PLAIN_TEXT,
                    None,
                ),
            ],
        )


class TestSplitNodeLinks(TestSplitNodeImagesLinksTestItems):
    def test_split_links(self):
        self.assertListEqual(
            split_nodes_link(self.two_images),
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.PLAIN_TEXT,
                    None,
                )
            ],
        )
        self.assertListEqual(
            split_nodes_link(self.two_links),
            [
                TextNode("This is text with ", TextType.PLAIN_TEXT, None),
                TextNode("two links", TextType.LINK, "http://foxpetters.org"),
                TextNode(" and including a new ", TextType.PLAIN_TEXT, None),
                TextNode("second link", TextType.LINK, "http://foxpetters2.org"),
            ],
        )
        self.assertListEqual(
            split_nodes_link(self.link_and_image),
            [
                TextNode(
                    "This is some text with ![an image](fox.png), but also includes ",
                    TextType.PLAIN_TEXT,
                    None,
                ),
                TextNode("a standard link", TextType.LINK, "http://foxpetters.org"),
            ],
        )


class TestTextToTextNode(unittest.TestCase):
    def setUp(self) -> None:
        self.text1 = "**bold** plain _italic_ `code` ![img](http://foxpetters.org) uheeee~ [link](http://atsuiyo.com)"

    def test_text_to_textnode(self):
        self.assertListEqual(
            text_to_textnodes(self.text1),
            [
                TextNode("bold", TextType.BOLD_TEXT, None),
                TextNode(" plain ", TextType.PLAIN_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
                TextNode(" ", TextType.PLAIN_TEXT, None),
                TextNode("code", TextType.CODE_TEXT, None),
                TextNode(" ", TextType.PLAIN_TEXT, None),
                TextNode("img", TextType.IMAGE, "http://foxpetters.org"),
                TextNode(" uheeee~ ", TextType.PLAIN_TEXT, None),
                TextNode("link", TextType.LINK, "http://atsuiyo.com"),
            ],
        )