import unittest
import scraper

class TestScraper(unittest.TestCase):
    def test_extract_next_links(self):
        scraper.extract_next_links()

if __name__ == '__main__':
    unittest.main()