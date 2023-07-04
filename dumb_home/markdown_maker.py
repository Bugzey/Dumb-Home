"""
Class to create web pages out of Markdown files
"""

import markdown

from dumb_home.base_maker import BaseMaker


class MarkdownMaker(BaseMaker):
    """
    Class to create Markdown files from text input
    """
    @classmethod
    def _make_body(cls, text: str) -> str:
        result = markdown.markdown(text)
        return result

    @classmethod
    def _make_header(cls) -> str:
        return ""

    @classmethod
    def _make_sidebar(cls) -> str:
        return ""

    @classmethod
    def _make_footer(cls) -> str:
        return ""

    @classmethod
    def _apply_template(cls, header: str, sidebar: str, body: str, footer: str) -> str:
        result = f"{header}{sidebar}{body}{footer}"
        return result

    @classmethod
    def make_page(cls, text: str) -> str:
        header = cls._make_header()
        sidebar = cls._make_sidebar()
        body = cls._make_body(text)
        footer = cls._make_footer()

        result = cls._apply_template(header, sidebar, body, footer)
        return result
