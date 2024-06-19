"""
Dumb home server
"""

from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import unquote

from flask import Flask, current_app, render_template, send_from_directory

from dumb_home.markdown_maker import MarkdownMaker
from dumb_home.navigation import Nav
from dumb_home.yaml_maker import YamlMaker

app = Flask(__name__)


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
            #   Just return the file
            return send_from_directory(base_path, path)

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
    app.root_path = app.config.file.absolute().parent
    app.static_folder = Path(__file__).parent / "static"
    app.template_folder = Path(__file__).parent / "templates"
    app.run(debug=args.debug)


if __name__ == "__main__":
    main()
