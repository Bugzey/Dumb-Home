"""
Abstract base class for the Maker class
"""

from abc import ABC, abstractmethod


class BaseMaker(ABC):
    @classmethod
    @abstractmethod
    def _make_header(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def _make_body(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def _make_sidebar(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def _make_footer(cls) -> str:
        pass
