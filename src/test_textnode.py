import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def setUp(self) -> None:
        self.textnode_plain = TextNode("Foxes", TextType.PLAIN_TEXT)
        self.textnode_plain_duplicate = TextNode("Foxes", TextType.PLAIN_TEXT)
        self.textnode_plain_with_link = TextNode("Foxes in Boxes", TextType.PLAIN_TEXT, "http://foxesinboxes.com")
        self.textnode_italic = TextNode("Foxes", TextType.ITALIC_TEXT)
        self.textnode_image = TextNode("Fox", TextType.IMAGE, "fox.jpg")
        self.textnode_link = TextNode("Foxes in Bath", TextType.LINK, "http://foxesinbath.moe")
        self.textnode_link_missing = TextNode("Foxes in Bath", TextType.LINK)

    def test_eq(self):
        self.assertEqual(self.textnode_plain, self.textnode_plain_duplicate)
        self.assertNotEqual(self.textnode_image, self.textnode_link)
        self.assertNotEqual(self.textnode_plain, self.textnode_plain_with_link)

    def test_repr(self):
        self.assertEqual(repr(self.textnode_plain), 'TextNode(Foxes, plain, None)')
        self.assertEqual(repr(self.textnode_plain_with_link), 'TextNode(Foxes in Boxes, plain, http://foxesinboxes.com)')