"""
Dumb home server
"""

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote

from flask import Flask, current_app, render_template
from typing_extensions import Self

from dumb_home.markdown_maker import MarkdownMaker
from dumb_home.yaml_maker import YamlMaker


app = Flask(__name__)


@dataclass
class Nav:
    name: str
    path: str

    @classmethod
    def from_path(cls, path: Path, base_path: Path) -> list[Self]:
        #   Create relative links
        data = []
        path = path.parent if path.is_file() else path
        for item in path.iterdir():
            if item.suffix not in (".md", ):
                continue
            data.append({"name": item.stem, "path": quote(str(item.relative_to(base_path)))})

        return [cls(**item) for item in data]


@app.route("/")
@app.route("/<path:path>")
def index(path: str = None):
    base_file = Path(current_app.config.file)
    base_path = base_file.parent
    cur_path = (base_path / unquote(path)) if path else base_file
    extension = cur_path.suffix.casefold()

    with open(cur_path, "r") as cur_file:
        if extension == ".md":
            content = MarkdownMaker.make_page(cur_file.read())
        elif extension in (".yaml", ".yml"):
            content = YamlMaker.make_page(cur_file.read())
        else:
            return f"Unsupported file type: {extension}", 400

    nav = Nav.from_path(path=cur_path, base_path=base_path)

    return render_template("page.html", content=content, nav=nav, title=cur_path.stem)


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="dumb_home")
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="File to serve as a landing page and whose parent directory is sourced for pages",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true", help="Start with verbose output and a debug server",
    )
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    app.config.file = Path(args.file).expanduser()
    app.run(debug=args.debug)


if __name__ == "__main__":
    main()
