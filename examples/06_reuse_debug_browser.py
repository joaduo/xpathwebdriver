'''
For running this test you need to first dump credentials.json
Can be done with command:
    xpathshell -d examples/credentials.json
'''
import unittest
from xpathwebdriver.default_settings import Settings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import WebdriverManager


class Settings(Settings):
    webdriver_browser = 'Chrome'
    webdriver_browser_keep_open = True
    webdriver_remote_credentials_path = 'credentials.json'

    #Alternatively instead of providing a path, you can directly paste executor url and session id
    #here. (remember to comment webdriver_remote_credentials_path line, or values below will be overriden)
    #Use xpathshell -p (to see them)
    #webdriver_remote_command_executor = ''
    #webdriver_remote_session_id = ''


class DuckDuckKeepOpenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())
        cls._mngr = WebdriverManager()

    @classmethod
    def tearDownClass(cls):
        del cls._mngr

    def test_duckduckgo(self):
        with self._mngr.enter_level() as browser: # Reuse the "outside" browser
            browser.get_url('https://duckduckgo.com/')
            with self._mngr.enter_level() as browser: # New browser
                browser.get_url('https://google.com/')


if __name__ == "__main__":
    unittest.main()
