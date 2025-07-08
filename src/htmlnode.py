class HTMLNode:
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self, props):
        if props is None:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in props.items()])

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        if self.tag == "br":
            return "<br>"
        
        attrs = ""
        if self.props:
            for prop, value in self.props.items():
                attrs += f' {prop}="{value}"'
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        if self.tag:
            return f"<{self.tag}{attrs}>{children_html}</{self.tag}>"
        else:
            return self.value or ""
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Leaf nodes must have a value")
        super().__init__(tag=tag, value=value, props=props)
        self.children = None
    
    def to_html(self):
        if self.tag == None:
            return self.value
        if self.tag == "br":
            return "<br>"
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html(self.props)}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            raise ValueError("Parent nodes must have children")
        if tag is None:
            raise ValueError("Parent nodes must have a tag")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.props == None:
            return f"<{self.tag}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html(self.props)}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"