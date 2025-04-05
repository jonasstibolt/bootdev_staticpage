import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "Hello, World!")
        node2 = HTMLNode("p", "Hello, World!")
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = HTMLNode("p", "Hello, World!")
        node2 = HTMLNode("div", "Hello, World!")
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        node1 = HTMLNode("p", "Hello, World!")
        node2 = HTMLNode("p", "Hello, World!", [HTMLNode("a", "https://www.example.com")])
        self.assertNotEqual(node1, node2)

    def test_eq2(self):
        node1 = HTMLNode("p", "Hello, World!", [HTMLNode("a", "https://www.example.com")], {"class": "text"})
        node2 = HTMLNode("p", "Hello, World!", [HTMLNode("a", "https://www.example.com")], {"class": "text"})
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main
