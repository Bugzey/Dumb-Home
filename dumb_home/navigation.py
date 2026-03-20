"""
Module go create a navigation item
"""

from dataclasses import dataclass, field
import os
from pathlib import Path
from urllib.parse import quote

from typing_extensions import Self


@dataclass
class NavItem:
    """
    Single navigation item in a navigation menu. Can be a directory or a file. The Nav class should
    store these
    """
    name: str
    path: str
    is_dir: bool
    is_open: bool

    @classmethod
    def from_path(cls, path: Path, base_path: Path, name_override: str | None = None) -> Self:
        return cls(
            name=name_override or path.stem,
            path=quote(str(Path("/") / path.relative_to(base_path))),
            is_dir=path.is_dir(),
            is_open=path.is_relative_to(base_path),
        )

    def __eq__(self, other):
        return (self.is_dir == other.is_dir) and (self.name == other.name)

    def __lt__(self, other):
        if self.is_dir and not other.is_dir:
            return True
        if not self.is_dir and other.is_dir:
            return False

        return self.name < other.name


@dataclass
class Nav:
    """
    Navigation menu useable by the navigation template. This presents a hierarchical folder
    structure of files and folders
    """
    location: list[NavItem] = field(default_factory=list)
    files: list[NavItem] = field(default_factory=list)
    folders: list[NavItem] = field(default_factory=list)

    extensions = (".md", ".yaml")

    @classmethod
    def check_file(cls, path: Path) -> bool:
        return (
            path.suffix in cls.extensions
            and not path.name.startswith(".")  # ignore hidden files
        )

    @classmethod
    def check_path(cls, path: Path) -> bool:
        for (_, folders, files) in os.walk(str(path)):
            if folders:
                return True

            if any(
                item.endswith(extension)
                for item
                in files
                for extension
                in cls.extensions
            ):
                return True

        return False

    @classmethod
    def from_path(cls, path: Path, base_path: Path, base_name: str | None = None) -> Self:
        nav = cls()

        #   Create parents
        if path.is_file():
            path = path.parent

        for item in (path, *path.parents):
            if not item.is_relative_to(base_path):
                break
            if item.name.startswith("."):  # ignore hidden folders
                break

            nav.location.append(
                NavItem.from_path(
                    item,
                    base_path,
                    name_override=base_name if item == base_path else None,
                )
            )

        nav.location.reverse()

        #   Create items
        for item in path.iterdir():
            if item.is_file() and cls.check_file(item):
                nav.files.append(NavItem.from_path(item, base_path))
            elif item.is_dir() and cls.check_path(item):
                nav.folders.append(NavItem.from_path(item, base_path))

        nav.files.sort()
        nav.folders.sort()

        return nav
