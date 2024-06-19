"""
Tests fro the navigation module
"""

from pathlib import Path
import tempfile
import unittest

from dumb_home.navigation import Nav


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

    def test_nav(self):
        result = Nav.from_path(
            path=Path(self.temp_dir.name) / "base/a.md",
            base_path=Path(self.temp_dir.name),
        )
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], Nav)
        self.assertIn(
            Nav(name="a", path="base/a.md", is_dir=False, is_open=True),
            result,
        )
        self.assertIn(
            Nav(name="subfolder", path="base/subfolder", is_dir=True, is_open=False),
            result,
        )
