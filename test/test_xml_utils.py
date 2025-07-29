# test_math_utils.py
import unittest
import base64

from pathlib import Path

import xml_utils

BASE_DIR = Path(__file__).parent
FIXTURE_DIR = BASE_DIR / "fixtures"


class TextXmlWatcher(unittest.TestCase):

    def test_get_parts_amount(self):
        expected = 2
        actual = len(xml_utils.find_parts(FIXTURE_DIR / "sample.xml"))
        self.assertEqual(actual, expected)

    def test_get_parts_content(self):
      actual_parts = xml_utils.find_parts(FIXTURE_DIR / "sample.xml")
      self.assertEqual(actual_parts[0].body, "This is a test.".encode("utf-8"))
      self.assertEqual(actual_parts[1].body, "This is a test too.".encode("utf-8"))

if __name__ == "__main__":
    unittest.main()
