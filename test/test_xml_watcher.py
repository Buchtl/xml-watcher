# test_math_utils.py
import unittest

from pathlib import Path

import xml_watcher

BASE_DIR = Path(__file__).parent
FIXTURE_DIR = BASE_DIR / "fixtures"

class TextXmlWatcher(unittest.TestCase):
    
    def test_get_parts(self):
        expected = 2
        actual = len(xml_watcher.find_parts(FIXTURE_DIR / "sample.xml"))
        self.assertEqual(actual, expected)
        

if __name__ == '__main__':
    unittest.main()
