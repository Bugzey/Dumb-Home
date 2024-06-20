"""
Class to create web pages out of Markdown files
"""
from dataclasses import dataclass, field

from markdown import Markdown

from dumb_home.base_maker import BaseMaker


EXTENSIONS = [
    "extra",
    "meta",
    "toc",
    "markdown_checklist.extension",
]
EXTENSION_KWARGS = {
    "toc": {
        "anchorlink": True,
    },
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
