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
        self.browser.fill('.//*[@name="q"]', 'xpathwebdriver\n')

    def test_duckduckgo_rel_imp(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill('.//*[@name="q"]', 'rel_imp python\n')


if __name__ == "__main__":
    unittest.main()
