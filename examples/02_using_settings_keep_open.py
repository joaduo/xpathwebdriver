import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.browser import Browser


class Settings(DefaultSettings):
    #Override here any desired option
    webdriver_browser = 'Chrome'
    # Force browser to survive testing (for inspection for example)
    webdriver_browser_keep_open = True


class DuckDuckKeepOpenTest(unittest.TestCase):
    """
    Also in this example we setup one browser for all tests
    """
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        del cls.browser

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')

    def test_duckduckgo_rel_imp(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'rel_imp python\n')


if __name__ == "__main__":
    register_settings_instance(Settings())
    unittest.main()
