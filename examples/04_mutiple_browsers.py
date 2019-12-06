import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import WebdriverManager


class Settings(DefaultSettings):
    #Override here any desired option check example 02
    pass


class DuckDuckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def test_duckduckgo(self):
        #Use WebdriverManager for more than 1 browser
        with WebdriverManager().enter_level(name='First') as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
            with WebdriverManager().enter_level(name='Second') as browser2:
                browser2.get_url('https://google.com/')


if __name__ == "__main__":
    unittest.main()
