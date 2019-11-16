import unittest
from xpathwebdriver.default_settings import Settings
from xpathwebdriver.levels import SINGLE_TEST_LIFE
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
    webdriver_browser_keep_open = False #a new browser on each test


class NewBrowserPerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def setUp(self):
        self._level_mngr = WebdriverManager().enter_level(level=SINGLE_TEST_LIFE, name=__name__)
        self.browser = self._level_mngr.__enter__()

    def tearDown(self):
        # Make sure we quit browser created for the specific test
        # If for some reason you would like to inspect the browser
        # add a pause here with ipdb or pdb eg: import pdb; pdb.set_trace()
        self._level_mngr.__exit__()

    def test_duckduckgo(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')

    def test_duckduckgo2(self):
        self.browser.get_url('https://duckduckgo.com/')
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'Second test\n')


if __name__ == "__main__":
    logging.basicConfig()
    #logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
