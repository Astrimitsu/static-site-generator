import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def setUp(self) -> None:
        self.leafnode_plain = LeafNode(None, "fox")

        self.leafnode_bold = LeafNode("b", "bold foxes")
        self.leafnode_one_prop = LeafNode(
            "a", "CLICK FOR MORE FOXES!", {"href": "http://morefoxes.net/fox.png"}
        )
        self.leafnode_three_props = LeafNode(
            "a",
            "Pettable Foxes Here",
            {
                "href": "https://foxpetters.net/petem",
                "target": "_blank",
                "id": "fox-link",
            },
        )
        self.leafnode_no_value = LeafNode(
            "a", None  # pyright: ignore[reportArgumentType]
        )

    def test_to_html(self):
        self.assertEqual(self.leafnode_plain.to_html(), "fox")
        self.assertEqual(self.leafnode_bold.to_html(), "<b>bold foxes</b>")
        self.assertEqual(
            self.leafnode_one_prop.to_html(),
            '<a href="http://morefoxes.net/fox.png">CLICK FOR MORE FOXES!</a>',
        )
        self.assertEqual(
            self.leafnode_three_props.to_html(),
            '<a href="https://foxpetters.net/petem" target="_blank" id="fox-link">Pettable Foxes Here</a>',
        )
        self.assertRaises(ValueError, self.leafnode_no_value.to_html)

    def test_repr(self):
        self.assertEqual(repr(self.leafnode_plain), "LeafNode(None, fox, None)")
        self.assertEqual(repr(self.leafnode_bold), "LeafNode(b, bold foxes, None)")
        self.assertEqual(
            repr(self.leafnode_one_prop),
            f"LeafNode(a, CLICK FOR MORE FOXES!, {self.leafnode_one_prop.props})",
        )
        self.assertEqual(
            repr(self.leafnode_three_props),
            f"LeafNode(a, Pettable Foxes Here, {self.leafnode_three_props.props})",
        )
