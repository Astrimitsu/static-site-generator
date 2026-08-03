from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError(f"Error: Value of {self!r} is None")
        if self.children is None:
            raise ValueError(f"Error: {self!r} has no children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"