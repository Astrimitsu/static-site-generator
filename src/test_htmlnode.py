import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def setUp(self) -> None:
        self.htmlnode_a = HTMLNode(
            props={"stuff": "things", "foxes": "boxes", "fox": "snacks"}
        )
        self.htmlnode_b = HTMLNode(
            props={"foo": "bar", "dog": "cat", "foxes": "are for petting"}
        )
        self.htmlnode_empty = HTMLNode()

    def test_to_html(self) -> None:
        self.assertRaises(NotImplementedError, self.htmlnode_a.to_html)
        self.assertRaises(NotImplementedError, self.htmlnode_b.to_html)

    def test_props_to_html(self) -> None:
        self.assertEqual(self.htmlnode_a.props_to_html(), ' stuff="things" foxes="boxes" fox="snacks"')
        self.assertEqual(self.htmlnode_b.props_to_html(), ' foo="bar" dog="cat" foxes="are for petting"')
        self.assertEqual(self.htmlnode_empty.props_to_html(), '')