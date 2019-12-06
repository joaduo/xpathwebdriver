import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.simple_xpath_browser import SimpleXpathBrowser


class Settings(DefaultSettings):
    #Override here any desired option
    # Check more details inspecting the DefaultSettings class
    # https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/default_settings.py#L12
    webdriver_browser = 'Chrome'
    # Force browser to survive testing (for inspection for example)
    webdriver_browser_keep_open = True


class DuckDuckKeepOpenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())
        cls.browser = SimpleXpathBrowser()

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
