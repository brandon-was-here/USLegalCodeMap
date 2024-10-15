import unittest
from bs4 import BeautifulSoup
from main.parser import parse_viewheader
from main.class_hierarchy import Section
import os

class TestParser(unittest.TestCase):
    def test_parse_viewheader(self):
        file_path = os.path.join("data", "section1182.xhtml")

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content,  'html.parser')

        section = parse_viewheader(soup)

        self.assertIsInstance(section, Section)
        self.assertEqual(section.number, "§1182")
        self.assertEqual(section.subchapter.number, "II")
        self.assertEqual(section.chapter.number, "12")
        self.assertEqual(section.title.number, "8")

if __name__ == "__main__":
    unittest.main()
