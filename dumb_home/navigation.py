"""
Module go create a navigation item
"""

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from typing_extensions import Self


@dataclass
class Nav:
    """
    Navigation menu useable by the navigation template. This presents a hierarchical folder
    structure of files and folders
    """
    name: str
    path: str
    is_dir: bool
    is_open: bool

    @classmethod
    def from_path(cls, path: Path, base_path: Path) -> list[Self]:
        #   Create relative links
        data = []
        for item in base_path.glob("**/*"):
            if item.is_file() and item.suffix not in (".md", ):
                continue
            data.append({
                "name": item.stem,
                "path": quote(str(item.relative_to(base_path))),
                "is_dir": item.is_dir(),
                "is_open": path.is_relative_to(item),
            })

        return sorted([cls(**item) for item in data], key=lambda x: (x.is_dir, x.path))
