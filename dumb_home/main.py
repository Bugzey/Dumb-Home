"""
Dumb home server
"""

from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import unquote

from flask import Flask, current_app, render_template, send_from_directory, abort

from dumb_home.markdown_maker import MarkdownMaker
from dumb_home.navigation import Nav
from dumb_home.yaml_maker import YamlMaker

PACKAGE_DIR = Path(__file__).parent
STATIC_DIR = PACKAGE_DIR / "static"
TEMPLATE_DIR = PACKAGE_DIR / "templates"

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    template_folder=TEMPLATE_DIR,
)


@app.route("/")
@app.route("/<path:path>")
def index(path: str = None):
    base_file = Path(current_app.config.file)
    base_path = Path(current_app.config.root_path)
    cur_path = (base_path / unquote(path)) if path else base_file
    cur_path = cur_path.absolute()
    extension = cur_path.suffix.casefold()

    if not cur_path.exists() or cur_path.name.startswith("."):
        abort(404)

    if cur_path.is_dir():
        nav = Nav.from_path(
            path=cur_path,
            base_path=base_path,
        )
        return render_template(
            "folder.html",
            title=cur_path.name,
            nav=nav,
        )

    with open(cur_path, "r") as cur_file:
        if extension == ".md":
            maker = MarkdownMaker(cur_file.read())
        elif extension in (".yaml", ".yml"):
            maker = YamlMaker(cur_file.read())
        else:
            #   Just return the file
            return send_from_directory(base_path, path)

    content = maker.make_body()
    sidebar = maker.make_sidebar()
    nav = Nav.from_path(
        path=cur_path,
        base_path=base_path,
    )

    return render_template(
        "page.html",
        content=content,
        nav=nav,
        title=cur_path.stem,
        sidebar=sidebar,
    )


@app.errorhandler(404)
def not_found(error):
    nav = Nav.from_path(
        path=app.config.root_path,
        base_path=app.config.root_path,
    )
    return render_template("404.html", nav=nav), 404


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="dumb_home")
    parser.add_argument(
        "target",
        help="Path or file as a root directory",
        type=lambda x: Path(x).expanduser().absolute(),
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

    if not args.target.exists():
        raise ValueError(f"Given target {args.target} does not exist")

    if args.target.is_dir():
        app.config.root_path = args.target
        app.config.file = args.target
    elif args.target.is_file():
        app.config.file = args.target
        app.config.root_path = args.target.parent
    else:
        raise ValueError("Invalid target - expected file or directory")

    app.run(debug=args.debug)


if __name__ == "__main__":
    main()
