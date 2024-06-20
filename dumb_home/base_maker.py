"""
Abstract base class for the Maker class
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMaker(ABC):
    content: str

    @abstractmethod
    def make_body(self) -> str:
        pass

    @abstractmethod
    def make_sidebar(self) -> str:
        pass
