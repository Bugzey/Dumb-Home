"""
"""

import unittest

from dumb_home.markdown_maker import MarkdownMaker


class MarkdownMakerTestCase(unittest.TestCase):
    def setUp(self):
        self.text="""# Some markdown file
##  Section
Bla bla text
in one paragraph

* Bullet 1
* Bullet 2"""

    def test_make_body(self):
        result = MarkdownMaker._make_body(self.text)
        self.assertTrue(isinstance(result, str))
        self.assertIn("<h1>", result)
        self.assertIn("<ul>", result)
