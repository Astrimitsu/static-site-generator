from textnode import TextNode, TextType
from pathlib import Path
import shutil


# for the purposes of the lesson, i am reconstructing recursive copying myself. realistically, pathlib can just do this itself though...
def copy_assets(source: Path, destination: Path) -> None:
    shutil.rmtree(destination)
    destination.mkdir()
    def copy_directory(directory: Path):
        for file in (source / directory).iterdir():
            if file.is_dir():
                (destination / file).mkdir()
                copy_directory(file)
            else:
                file.copy(destination / file)





def main() -> None:
    static_dir = Path("static")
    public_dir = Path("public")
    print(list(public_dir.iterdir()))
main()
