import unittest
from xpathwebdriver.browser import Browser


class DuckDuckBasic(unittest.TestCase):
    def setUp(self):
        self.browser = Browser()

    def tearDown(self):
        # Make sure we quit browser
        del self.browser

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        # Type xpathwebdriver and press enter
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')


if __name__ == "__main__":
    import logging
    logging.basicConfig()
    #logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
