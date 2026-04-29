
class HTMLNode:
    def __init__(self,tag=None,value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_string = ""
        if self.props:
            for key in self.props:
                value = self.props[key]
                html_string += f' {key}="{value}"'
        return html_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value},children: {self.children},{self.props})"
    
    def __eq__(self,other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value},{self.props})"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("tag is required")
        if self.children == None:
            raise ValueError("children nodes require values")
        html_string = f"<{self.tag}>"
        for child_node in self.children:
            html_string+=child_node.to_html()
        html_string+=f"</{self.tag}>"
        return html_string
    
