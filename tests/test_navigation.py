"""
Tests fro the navigation module
"""

from pathlib import Path
import tempfile
import unittest

from dumb_home.navigation import (
    NavItem,
    Nav,
)


class NavItemTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file = Path(self.temp_dir.name) / "some file.extension"
        self.file.touch()
        self.folder = Path(self.temp_dir.name) / "some folder"
        self.folder.mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_from_path_file(self):
        result = NavItem.from_path(self.file, base_path=Path(self.temp_dir.name))
        self.assertIsInstance(result, NavItem)
        self.assertEqual(result.name, "some file")
        self.assertEqual(result.path, "some%20file.extension")
        self.assertFalse(result.is_dir)

    def test_from_path_folder(self):
        result = NavItem.from_path(self.folder, base_path=Path(self.temp_dir.name))
        self.assertIsInstance(result, NavItem)
        self.assertEqual(result.name, "some folder")
        self.assertEqual(result.path, "some%20folder")
        self.assertTrue(result.is_dir)


class NavTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folders = [
            "base",
            "base/subfolder",
            "base/empty_folder",
        ]
        self.files = [
            "base/a.md",
            "base/a.unsupported",
            "base/subfolder/item.md",
        ]
        for item in self.folders:
            item = Path(self.temp_dir.name) / item
            item.mkdir(parents=True, exist_ok=True)

        for item in self.files:
            item = Path(self.temp_dir.name) / item
            item.touch(exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_check_file(self):
        self.assertTrue(Nav.check_file(Path("a.md")))
        self.assertFalse(Nav.check_file(Path("a.unsupported")))

    def test_check_path(self):
        self.assertTrue(Nav.check_path(Path(self.temp_dir.name) / "base"))
        self.assertTrue(Nav.check_path(Path(self.temp_dir.name) / "base" / "subfolder"))
        self.assertFalse(Nav.check_path(Path(self.temp_dir.name) / "base" / "empty_folder"))

    def test_nav(self):
        result = Nav.from_path(
            path=Path(self.temp_dir.name) / "base",
            base_path=Path(self.temp_dir.name) / "base",
        )
        self.assertIsInstance(result, Nav)
        self.assertEqual(len(result.location), 1)
        self.assertEqual(result.location[0].name, "base")
        self.assertTrue(any(item.path == "a.md" for item in result.files))
        self.assertFalse(any(item.path == "a.unsupported" for item in result.files))
        self.assertFalse(any(item.path == "base/empty_folder" for item in result.folders))
