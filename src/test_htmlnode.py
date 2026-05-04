import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode,TextType,text_node_to_html_node
from extracttitle import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p","this is a value", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com"')
    
    def test_2(self):
        node3 = HTMLNode("h1","value")
        self.assertEqual(node3.tag,"h1")

    def test_3(self):
        node6=HTMLNode("h1","not a real value")
        self.assertNotEqual(node6.value,"not")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_2(self):
        node = LeafNode("h1","what's good ppl")
        self.assertEqual(node.to_html(), "<h1>what's good ppl</h1>")
    
    def test_leaf_to_html_3(self):
        node = LeafNode("p","this is a paragraph")
        self.assertNotEqual(node.to_html(),"<p>this is not a paragraph</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("d", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><d>grandchild</d></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text3(self):
        node = TextNode("This is a text node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href":None})

    def test_image_no_alt(self):
        node = TextNode("", TextType.IMAGE, "https://example.com/pic.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/pic.png")
        self.assertEqual(html_node.props["alt"], '')

    def test_extract_title_1(self):
        title = extract_title(
    "Some intro\n"
    "\n"
    "# My Title\n"
    "\n"
    "Body text"
)
        self.assertEqual(title, "My Title")

    def test_extract_title_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("there is no \n ## title in here")
