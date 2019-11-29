import unittest
from xpathwebdriver.default_settings import Settings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import WebdriverManager
import logging
from xpathwebdriver.levels import TEST_ROUND_LIFE


class Settings(Settings):
    virtual_display_enabled = False
    #virtual_display_backend = 'xvnc'
    virtual_display_size = (800, 600)
    virtual_display_visible = True
    virtual_display_keep_open = True

    webdriver_browser = 'Chrome'
    webdriver_browser_keep_open = False


class DuckDuckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())
        cls._mngr = WebdriverManager()
        cls._browser_context = cls._mngr.enter_level(level=TEST_ROUND_LIFE)
        cls.browser = cls._browser_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._browser_context.__exit__()
        del cls._mngr

    def test_duckduckgo(self):
        driver = self.browser.get_driver()
        driver.get('https://duckduckgo.com')
        element = driver.find_element_by_id('search_form_input_homepage')
        element.send_keys('Example')
        
            
if __name__ == "__main__":
    logging.basicConfig()
    #logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
