import unittest
from xpathwebdriver.default_settings import Settings
from xpathwebdriver.levels import TEST_ROUND_LIFE
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import WebdriverManager


class Settings(Settings):
    virtual_display_enable = False # If true, put browser in a contained window
    #virtual_display_backend = 'xvnc' # If you want to run in a remote server
    virtual_display_size = (800, 600)
    virtual_display_visible = True # Useful only when backend is not xvnc
    virtual_display_keep_open = True # If we want to check results (useful whe combined with webdriver_browser_keep_open)

    webdriver_browser = 'Chrome'
    #webdriver_browser = 'Firefox'
    #webdriver_browser = 'PhantomJS'
    webdriver_browser_keep_open = True #Survive or not after finishing


class DuckDuckKeepOpenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())
        cls._mngr = WebdriverManager()
        cls._level_mngr = cls._mngr.enter_level(level=TEST_ROUND_LIFE)
        cls.browser = cls._level_mngr.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._level_mngr.__exit__()
        del cls._mngr

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')

    def test_duckduckgo2(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'Second test\n')


if __name__ == "__main__":
    unittest.main()
