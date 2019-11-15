import unittest
from xpathwebdriver.default_settings import Settings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import WebdriverManager
import logging


class Settings(Settings):
    virtual_display_enable = False
    #virtual_display_backend = 'xvnc'
    virtual_display_size = (800, 600)
    virtual_display_visible = True
    virtual_display_keep_open = True

    webdriver_browser = 'Chrome'
    webdriver_browser_keep_open = False

    log_color = True


class DuckDuckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())
        cls._mngr = WebdriverManager()

    @classmethod
    def tearDownClass(cls):
        del cls._mngr

    def test_duckduckgo(self):
        with self._mngr.enter_level(name='First') as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
            with self._mngr.enter_level(name='Second') as browser2:
                self._test_google(browser2)

    def _test_google(self, browser):
        browser.get_url('https://google.com/')

if __name__ == "__main__":
    logging.basicConfig()
    #logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
