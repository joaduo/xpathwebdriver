import unittest
from xpathwebdriver.browser import Browser


class DuckDuckBasic(unittest.TestCase):
    """
    In this example we show how use setup and tearDown methods.
    If for some reason we want to avoid context manager as used in example 00_...

    We create a new browser for each test.
    """
    def setUp(self):
        self.browser = Browser()

    def tearDown(self):
        # Make sure we quit browser
        del self.browser

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        # Type xpathwebdriver and press enter
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')

    def test_duckduckgo_rel_imp(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'rel_imp python\n')


if __name__ == "__main__":
    unittest.main()
