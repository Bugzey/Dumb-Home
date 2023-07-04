"""
Dumb home server
"""

from argparse import ArgumentParser
from pathlib import Path

from flask import Flask, current_app

from dumb_home.markdown_maker import MarkdownMaker
from dumb_home.yaml_maker import YamlMaker


app = Flask(__name__)
app.config.file: Path = Path().home() / "Desktop" / "todo.md"


@app.route("/")
def index():
    cur_path = current_app.config.file
    extension = cur_path.suffix.casefold()

    with open(cur_path, "r") as cur_file:
        if extension == ".md":
            result = MarkdownMaker.make_page(cur_file.read())
        elif extension in (".yaml", ".yml"):
            result = YamlMaker.make_page(cur_file.read())
        else:
            return f"Unsupported file type: {extension}", 400

    return result


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="dumb_home")
    parser.add_argument("-f", "--file")
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    if args.file:
        app.config.file = Path(args.file)
    app.run()


if __name__ == "__main__":
    main()
