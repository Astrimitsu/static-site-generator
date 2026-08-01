from textnode import TextNode, TextType


def main() -> None:
    text = TextNode("MORE Foxes", TextType.LINK, "http://cutefoxes.moe")
    print(repr(text))


main()
