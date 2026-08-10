import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def setUp(self) -> None:
        self.textnode_plain = TextNode("Foxes", TextType.PLAIN_TEXT)
        self.textnode_plain_duplicate = TextNode("Foxes", TextType.PLAIN_TEXT)
        self.textnode_plain_with_link = TextNode(
            "Foxes in Boxes", TextType.PLAIN_TEXT, "http://foxesinboxes.com"
        )
        self.textnode_italic = TextNode("Foxes", TextType.ITALIC_TEXT)
        self.textnode_image = TextNode("Fox", TextType.IMAGE, "fox.jpg")
        self.textnode_link = TextNode(
            "Foxes in Bath", TextType.LINK, "http://foxesinbath.moe"
        )
        self.textnode_link_missing = TextNode("Foxes in Bath", TextType.LINK)

    def test_textnode_to_htmlnode(self):
        self.assertEqual(
            text_node_to_html_node(self.textnode_plain), LeafNode(None, "Foxes", None)
        )
        self.assertEqual(
            text_node_to_html_node(self.textnode_plain_with_link),
            LeafNode(None, "Foxes in Boxes", None),
        )
        self.assertEqual(
            text_node_to_html_node(self.textnode_italic), LeafNode("i", "Foxes", None)
        )
        self.assertEqual(
            text_node_to_html_node(self.textnode_image),
            LeafNode("img", None, {"src": "fox.jpg", "alt": "Fox"}),
        )
        self.assertEqual(
            text_node_to_html_node(self.textnode_link),
            LeafNode("a", "Foxes in Bath", {"href": "http://foxesinbath.moe"}),
        )
        self.assertRaises(
            ValueError, text_node_to_html_node, self.textnode_link_missing
        )

    def test_eq(self):
        self.assertEqual(self.textnode_plain, self.textnode_plain_duplicate)
        self.assertNotEqual(self.textnode_image, self.textnode_link)
        self.assertNotEqual(self.textnode_plain, self.textnode_plain_with_link)

    def test_repr(self):
        self.assertEqual(repr(self.textnode_plain), "TextNode(Foxes, TextType.PLAIN_TEXT, None)")
        self.assertEqual(
            repr(self.textnode_plain_with_link),
            "TextNode(Foxes in Boxes, TextType.PLAIN_TEXT, http://foxesinboxes.com)",
        )
