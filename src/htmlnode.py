class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ""

        if self.props:
            for prop, value in self.props.items():
                output += f" {prop}=\"{value}\""

        return output
    
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"     
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError

        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return str(self.value)

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.props}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node missing tag")
        if self.children is None:
            raise ValueError("Parent node missing children")
        
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += f"{child.to_html()}"
        html += f"</{self.tag}>"

        return html