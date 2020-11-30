import unittest
from xpathwebdriver.browser import Browser


class NewBrowserPerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        del cls.browser

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')

    def test_duckduckgo2(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'Second test\n')


if __name__ == "__main__":
    unittest.main()
