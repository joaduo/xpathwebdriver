import unittest
from xpathwebdriver.simple_xpath_browser import SimpleXpathBrowser
import logging


class DuckDuckBasic(unittest.TestCase):
    def setUp(self):
        self.browser = SimpleXpathBrowser()

    def tearDown(self):
        # Make sure we quit browser
        del self.browser

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        # Type xpathwebdriver and press enter
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')


if __name__ == "__main__":
    logging.basicConfig()
    #logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()