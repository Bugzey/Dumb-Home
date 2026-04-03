"""
Class to create web pages out of Markdown files
"""
from dataclasses import dataclass, field

from markdown import Markdown
from pymdownx import emoji

from dumb_home.base_maker import BaseMaker


EXTENSIONS = [
    "admonition",
    "extra",
    "meta",
    "toc",
    "pymdownx.emoji",
    "pymdownx.tasklist",
]
EXTENSION_KWARGS = {
    "toc": {
        "anchorlink": True,
    },
    "pymdownx.emoji": {
        "emoji_index": emoji.twemoji,
    }
}


@dataclass
class MarkdownMaker(BaseMaker):
    """
    Class to create Markdown files from text input
    """
    _markdown: Markdown = field(init=False, default=None)

    @staticmethod
    def _make_markdown():
        return Markdown(extensions=EXTENSIONS, extension_configs=EXTENSION_KWARGS)

    def make_body(self) -> str:
        if not self._markdown:
            self._markdown = self._make_markdown()
        return self._markdown.convert(self.content)

    def make_sidebar(self) -> str:
        if not self._markdown:
            self._markdown = self._make_markdown()
            _ = self._markdown.convert(self.content)
        return self._markdown.toc
