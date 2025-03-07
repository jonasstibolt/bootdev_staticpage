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

if __name__ == "__main__":
    unittest.main()