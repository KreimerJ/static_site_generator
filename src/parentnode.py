from typing import override

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")

        children_format: str = ""
        for child in self.children:
            children_format += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_format}</{self.tag}>"
