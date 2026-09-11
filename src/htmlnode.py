from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError("Class should override this method")

    def props_to_html(self) -> str | None:
        html_format: str = ""
        if not self.props:
            return html_format
        if self.props:
            for key, value in self.props.items():
                html_format += f' {key}="{value}"'
            return html_format

    @override
    def __repr__(self) -> str:
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"
