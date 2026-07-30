import textnode


def main() -> None:
    text = textnode.TextNode(
        "MORE Foxes", textnode.TextType.LINK, "http://cutefoxes.moe"
    )
    print(repr(text))


main()
