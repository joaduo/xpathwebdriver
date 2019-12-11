import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.browser import Browser


class Settings(DefaultSettings):
    #Override here any desired option check example 02
    pass


class NewBrowserPerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def setUp(self):
        self.browser = Browser()

    def tearDown(self):
        del self.browser

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')

    def test_duckduckgo2(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'Second test\n')


if __name__ == "__main__":
    unittest.main()
