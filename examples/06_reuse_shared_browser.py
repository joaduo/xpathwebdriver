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


class DuckDuckKeepOpenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def test_duckduckgo(self):
        with get_browser() as browser: # Reuse the "outside" browser
            browser.get_url('https://duckduckgo.com/')


if __name__ == "__main__":
    unittest.main()
