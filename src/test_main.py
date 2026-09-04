import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def setUp(self) -> None:
        self.test1 = "# title1 \ntexttexttext"
        self.test2 = "text text text\n# title2"
        self.test3 = "no title :("

    def test_extract_title(self):
        self.assertEqual(extract_title(self.test1), "title1")
        self.assertEqual(extract_title(self.test2), "title2")
        self.assertRaises(ValueError, extract_title, self.test3)