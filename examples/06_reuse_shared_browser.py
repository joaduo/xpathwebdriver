'''
For running this test you need to first dump credentials.json
Can be done with command:
    xpathshell -d path/to/dumped/credentials.json
'''
import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import get_browser


class Settings(DefaultSettings):
    webdriver_remote_credentials_path = 'path/to/dumped/credentials.json'

    #Alternatively instead of providing a path, you can directly paste executor url and session id
    #here. (remember to comment webdriver_remote_credentials_path line, or values below will be overriden)
    # Run `xpathshell -p` (to see them and copy paste them)
    #webdriver_remote_command_executor = ''
    #webdriver_remote_session_id = ''


class DuckDuckKeepOpenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def test_duckduckgo(self):
        with get_browser() as browser: # Reuse the "outside" browser
            browser.get_url('https://duckduckgo.com/')


if __name__ == "__main__":
    unittest.main()
