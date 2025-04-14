import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Hello, World!", TextType.BOLD)
        node2 = TextNode("Hello, World!", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = TextNode("Hello, World!", TextType.BOLD)
        node2 = TextNode("Hello, World!", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        node1 = TextNode("Hello, World!", TextType.BOLD, "https://www.example.com")
        node2 = TextNode("Hello, World!", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_to_html(self):
        node = TextNode("Hello, World!", TextType.BOLD)
        self.assertEqual(node.text_node_to_html(), "<b>Hello, World!</b>")

    def test_to_html_with_url(self):
        node = TextNode("Example", TextType.LINK, "https://www.example.com")
        self.assertEqual(node.text_node_to_html(), '<a href="https://www.example.com">Example</a>')

if __name__ == "__main__":
    unittest.main()