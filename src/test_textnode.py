import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extract_links import extract_markdown_images,extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_2(self):
        node1 = TextNode("Bananas", TextType.ITALIC)
        node3 = TextNode("Bananas", TextType.ITALIC)
        self.assertEqual(node1,node3)

    def test_3(self):
        node5 = TextNode("Peanut Butter", TextType.BOLD)
        node6 = TextNode("Jelly",TextType.BOLD)
        self.assertNotEqual(node5,node6)

    def test_4(self):
        node7 = TextNode("Rubbish",TextType.BOLD)
        node8 = TextNode("Rubbish", TextType.ITALIC)
        self.assertNotEqual(node7,node8)

    def test_final(self):
        node9 = TextNode("this shouldnt work",TextType.BOLD)
        node10 = TextNode("or should it",TextType.ITALIC,"url.something")
        self.assertNotEqual

    def test_node_split_1(self):
        old_nodes = [TextNode("this is a **bold test** here",TextType.TEXT),TextNode("This is a plain node",TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        self.assertEqual(result,[TextNode("this is a ", TextType.TEXT, None),
                                    TextNode("bold test", TextType.BOLD, None),
                                    TextNode(" here", TextType.TEXT, None),
                                    TextNode("This is a plain node", TextType.TEXT, None)]) 


    def test_node_split_2(self):
        old_nodes = [TextNode("this is just text",TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes,"_",TextType.ITALIC)
        self.assertEqual(result,[TextNode("this is just text", TextType.TEXT, None)])

    def test_node_split_3(self):
        old_nodes = [TextNode("**YOU CAN'T HANDLE THE BANANAS**",TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes,"**", TextType.BOLD)
        self.assertEqual(result, [TextNode("**YOU CAN'T HANDLE THE BANANAS**",TextType.BOLD, None)])


    def test_image_extraction_1(self):
        compared_item = extract_markdown_images("There once was a ship that put to sea. the name of this ship was ![ship](https://www.freepik.com/clipart)")
        self.assertEqual(compared_item, [("ship","https://www.freepik.com/clipart")])


    def test_link_extraction_1(self):
        compared_item = extract_markdown_links("on this site is a helpful resource to learn[to education](https://www.bootdev.com)")
        self.assertEqual(compared_item, [("to education", "https://www.bootdev.com")])

    def test_image_multi(self):
        compared_item = extract_markdown_images("This is the multi test ![first ref](https://www.somethingrandom.com) and the 2nd refrence ![2nd ref](https://www.otherrandomlink.com) ")
        self.assertEqual(compared_item, [("first ref","https://www.somethingrandom.com"),("2nd ref","https://www.otherrandomlink.com")])



    def test_split_image_1(self):
        split_image_list = split_nodes_image([TextNode("this is an image test ![image goes here](https://www.someurlwithanimage.com)",TextType.TEXT),TextNode("This is the 2nd part but no image this time",TextType.TEXT)])
        self.assertEqual(split_image_list, [
            TextNode("this is an image test ", TextType.TEXT, None), 
            TextNode("image goes here",TextType.IMAGE, "https://www.someurlwithanimage.com"), 
            TextNode("This is the 2nd part but no image this time",TextType.TEXT, None)])


    def test_split_link_1(self):
        split_link_list = split_nodes_link([TextNode("this is a url test [the url goes here](https://www.thisistotallyaurl.com) and some text after for good measure")])
        self.assertEqual(split_link_list,[TextNode("this is a url test",TextType.TEXT, None),
                                          TextNode("the url goes here", TextType.LINK, "https://www.thisistotallyaurl.com"),
                                          TextNode("and some text after for good measure", TextType.TEXT, None)])

    def test_split_link_1(self):
        split_link_list = split_nodes_link([TextNode("this is to see if we just pass with no link provided", TextType.TEXT)])
        self.assertEqual(split_link_list, [TextNode("this is to see if we just pass with no link provided", TextType.TEXT, None)])


if __name__ == "__main__":
    unittest.main()