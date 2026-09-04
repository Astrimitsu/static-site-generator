import re
import shutil
import sys
from pathlib import Path

from splitblocks import markdown_to_html_node


class WebsiteGenerator:
    def __init__(
        self, source: Path, destination: Path, template: Path, base_path: str | None
    ) -> None:
        self.source: Path = source
        self.destination: Path = destination
        self.template: Path = template
        self.base_path: str | None = base_path

    def _scan_source(self, directory: Path = Path(".")):
        for file in (self.source / directory).iterdir():
            rel_dir = file.relative_to(self.source)
            if file.is_dir():
                (self.destination / rel_dir).mkdir(exist_ok=True)
                self._scan_source(rel_dir)
                print(f"Copied Directory: {self.destination / rel_dir!s}")
            elif file.suffix == ".md":
                self._generate_page(
                    (self.source / rel_dir), (self.destination / rel_dir)
                )
                print(f"Generated HTML: {self.destination / rel_dir!s}")
            else:
                file.copy(self.destination / rel_dir)
                print(f"Copied File: {self.destination / rel_dir!s}")

    def _generate_page(self, source: Path, destination: Path) -> None:
        with open(source) as f:
            markdown = f.read()
        with open(self.template) as f:
            template_html = f.read()

        titled = template_html.replace("{{ Title }}", extract_title(markdown))
        html = titled.replace(
            "{{ Content }}", markdown_to_html_node(markdown).to_html()
        )
        if self.base_path:
            finished_html = self.replace_base_path(html)
        else:
            finished_html = html

        destination.parent.mkdir(parents=True, exist_ok=True)

        with open(destination.with_suffix(".html"), mode="w") as f:
            f.write(finished_html)

    def run(self):
        self._scan_source()

    def replace_base_path(self, html: str) -> str:
        replaced_images = html.replace('href="/', f'href="{self.base_path!s}')
        replaced_links = replaced_images.replace('src="/', f'src="{self.base_path!s}')
        return replaced_links


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if re.match(r"^# .+", line):
            return line.removeprefix("# ").strip()
    raise ValueError("No title found")


def main() -> None:

    build = False
    base_path = None
    static_dir = Path("static")
    content_dir = Path("content")
    template = Path("template.html")

    args = iter(sys.argv[1:])
    for arg in args:
        if arg == "--build":
            build = True
        elif arg == "--basepath":
            try:
                arg_value = next(args)
                if arg_value.startswith("--"):
                    print("Usage: main.py [--basepath <site root>] [--build]")
                    sys.exit(64)
                base_path = arg_value
            except StopIteration:
                print("Missing argument: No path after --basepath")
                print("Usage: main.py [--basepath <site root>] [--build]")
                sys.exit(64)
        else:
            print("Usage: main.py [--basepath <site root>] [--build]")
            sys.exit(64)

    if build:
        output_directory = Path("docs")
    else:
        output_directory = Path("public")

    if output_directory.exists():
        shutil.rmtree(output_directory)
    output_directory.mkdir()

    WebsiteGenerator(static_dir, output_directory, template, base_path).run()
    WebsiteGenerator(content_dir, output_directory, template, base_path).run()


if __name__ == "__main__":
    main()
