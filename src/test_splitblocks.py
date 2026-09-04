import unittest

from splitblocks import markdown_to_blocks, markdown_to_html_node


import unittest

from splitblocks import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def setUp(self) -> None:
        self.paragraph = "Text item, should be a paragraph. \nThis is a newline."
        self.heading = "###### This should be a header"
        self.invalid_header = "####### This has too many pounds."
        self.code = "```\n This is a code block \n```"
        self.invalid_code = "```\n This has too qfew lines```"
        self.quote = "> Quote Text\n>Nospace\n> Quote2"
        self.invalid_quote = "> quote text\nNo quote beginning here."
        self.single_quote = "> Quote"
        self.unordered_list = "- bulleted list\n- item2\n- item3"
        self.ordered_list = "1. Item1 \n2. Item2\n3. item3\n4. item4"
        self.invalid_ordered_list = "1. Item1\n3. Item2"

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type(self.paragraph), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(self.heading), BlockType.HEADING)
        self.assertEqual(block_to_block_type(self.invalid_header), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(self.code), BlockType.CODE)
        self.assertEqual(block_to_block_type(self.invalid_code), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(self.quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(self.single_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(self.invalid_quote), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type(self.unordered_list), BlockType.UNORDERED_LIST
        )
        self.assertEqual(block_to_block_type(self.ordered_list), BlockType.ORDERED_LIST)
        self.assertEqual(
            block_to_block_type(self.invalid_ordered_list), BlockType.PARAGRAPH
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )