import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("p", "Hello, World!")
        node2 = LeafNode("p", "Hello, World!")
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = LeafNode("p", "Hello, World!")
        node2 = LeafNode("div", "Hello, World!")
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        node1 = LeafNode("p", "Hello, World!")
        node2 = LeafNode("p", "Hello, World!", {"class": "text"})
        self.assertNotEqual(node1, node2)

    def test_eq2(self):
        node1 = LeafNode("p", "Hello, World!", {"class": "text"})
        node2 = LeafNode("p", "Hello, World!", {"class": "text"})
        self.assertEqual(node1, node2)

    def test_eq_not_tag(self):
        node1 = LeafNode(value="Hello, World!")
        node2 = LeafNode(value="Hello, World!")
        self.assertEqual(node1, node2)

    def test_leaf_node_to_html(self):
        node = LeafNode("p", "Hello, World!", {"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello, World!</p>')

    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode(value="Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')

    def test_to_html_with_no_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main
