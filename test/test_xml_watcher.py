# test_math_utils.py
import unittest

from pathlib import Path

import xml_watcher

BASE_DIR = Path(__file__).parent
FIXTURE_DIR = BASE_DIR / "fixtures"


class TextXmlWatcher(unittest.TestCase):

    def test_something(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
