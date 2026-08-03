import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
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

        self.parentnode_no_children = ParentNode(
            "p", None, None  # pyright: ignore[reportArgumentType]
        )
        self.parentnode_no_tag = ParentNode(
            None,  # pyright: ignore[reportArgumentType]
            [],
            None,
        )
        self.parentnode_one_child = ParentNode("p", [self.leafnode_plain], None)
        self.parentnode_nested_children = ParentNode("div", [self.parentnode_one_child], None)
        self.parentnode_multiple_children = ParentNode("b", [self.leafnode_plain, self.leafnode_three_props], None)

    def test_to_html(self):
        self.assertRaises(ValueError, self.parentnode_no_children.to_html)
        self.assertEqual(self.parentnode_one_child.to_html(), "<p>fox</p>")
        self.assertEqual(self.parentnode_multiple_children.to_html(), '<b>fox<a href="https://foxpetters.net/petem" target="_blank" id="fox-link">Pettable Foxes Here</a></b>')
        self.assertEqual(self.parentnode_nested_children.to_html(), "<div><p>fox</p></div>")