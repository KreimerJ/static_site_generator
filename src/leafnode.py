from typing import override

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, props=props)

    @override
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")

        if not self.tag:
            return self.value

        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag = {self.tag}, value = {self.value},  props = {self.props})"
        )
