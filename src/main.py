from textnode import TextNode, TextType


def main():
    new_text_node: TextNode = TextNode(
        "This is some anchor tex", TextType.LINK, "https://www.boot.dev"
    )
    print(new_text_node)


if __name__ == "__main__":
    main()
