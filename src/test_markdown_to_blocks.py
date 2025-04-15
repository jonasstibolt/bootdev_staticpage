import unittest, textwrap
from functions import *
from textnode import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_block_to_lines(self):
        md = textwrap.dedent("""
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_empty_input(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_single_block(self):
        blocks = markdown_to_blocks("Just one block")
        self.assertEqual(blocks, ["Just one block"])

    def test_multiple_blank_lines(self):
        blocks = markdown_to_blocks("Block 1\n\n\n\nBlock 2")
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_leading_trailing_blank_lines(self):
        blocks = markdown_to_blocks("\n\n\nBlock 1\n\nBlock 2\n\n\n")
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_different_markdown_blocks(self):
        md = "# Heading\n\n> Blockquote\n\n```\ncode block\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "> Blockquote", "```\ncode block\n```"])

if __name__ == '__main__':
    unittest.main()