import unittest
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # Test case with a single node containing delimiters
        nodes = [TextNode("Hello *World*!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("World", TextType.BOLD),
            TextNode("!", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        # Test case with no delimiters
        nodes = [TextNode("Hello World!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [TextNode("Hello World!", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)
    
    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links(
            "This is text without a link"
        )
        self.assertListEqual([], matches)

    def test_link_and_image_extraction(self):
        test_text = """
        This is a regular [link](https://example.com) and this is an ![image](https://example.com/image.jpg)
        """
        
        # Test link extraction
        links = extract_markdown_links(test_text)
        expected_links = [('link', 'https://example.com')]
        self.assertEqual(expected_links, links, "Link extraction failed")
        
        # Test image extraction
        images = extract_markdown_images(test_text)
        expected_images = [('image', 'https://example.com/image.jpg')]
        self.assertEqual(expected_images, images, "Image extraction failed")

    #test split image nodes
    def test_split_image_node(self):
        node = TextNode("This is an ![image](https://example.com/image.jpg) here", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_link_node(self):
        node = TextNode("This is a [link](https://example.com/image.jpg)", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/image.jpg"),
        ]
        self.assertEqual(result, expected)
        
    def test_text_to_textnodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        result = text_to_textnodes(node.text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()