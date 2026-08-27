import unittest

from splitblocks import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def setUp(self) -> None:
        self.paragraph = "Text item, should be a paragraph. \nThis is a newline."
        self.heading = "###### This should be a header"
        self.invalid_header = "####### This has too many pounds."
        self.code = "```\n This is a code block \n```"
        self.invalid_code = "```\n This has too few lines```"
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
        self.assertEqual(block_to_block_type(self.unordered_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(self.ordered_list), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(self.invalid_ordered_list), BlockType.PARAGRAPH)