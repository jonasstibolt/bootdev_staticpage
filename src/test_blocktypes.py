import unittest
from functions import *
from textnode import *
from blocktypes import *

class TestBlocktypes(unittest.TestCase):
    def test_block_to_blocktype_heading(self):
        test = "# Heading\n\n> Blockquote\n\n```\ncode block\n```"
        expected = BlockType.HEADING
        result = block_to_block_type(test)
        self.assertEqual(expected, result)

    def test_block_to_blocktype_code(self):
        test = "```\ncode block\n```"
        expected = BlockType.CODE
        result = block_to_block_type(test)
        self.assertEqual(expected, result)

    def test_block_to_blocktype_quote(self):
        test = ">Blockquote\n>code block"
        expected = BlockType.QUOTE
        result = block_to_block_type(test)
        self.assertEqual(expected, result)

    def test_block_to_blocktype_ulist(self):
        test = "- list item\n- item \n- item again"
        expected = BlockType.UNORDERED_LIST
        result = block_to_block_type(test)
        self.assertEqual(expected, result)

    def test_block_to_blocktype_olist(self):
        test = "1. item\n2. item\n3. item"
        expected = BlockType.ORDERED_LIST
        result = block_to_block_type(test)
        self.assertEqual(expected, result)

    def test_block_to_blocktype_p(self):
        test = "This is a **bolded** paragraph"
        expected = BlockType.PARAGRAPH
        result = block_to_block_type(test)
        self.assertEqual(expected, result)

    # def test_block_to_blocktype_error(self):
    #     test = ""
    #     expected = Exception("invalid markdown format")
    #     result = block_to_block_type(test)
    #     self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()