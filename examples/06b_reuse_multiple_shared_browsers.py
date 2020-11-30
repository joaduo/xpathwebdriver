'''
Dump credentials.json for the first browser
By if not set --context-name will be 'default'
    xpathshell -d credentials.json
In another terminal run a second browser that will be shared
Set the context name to something else ('firefox' in this case)
    export XPATHWD_WEBDRIVER_BROWSER="Firefox"; xpathshell -d credentials.json -c firefox
Then run this test
Fix webdriver_remote_credentials_path value in settings if needed
    python3 examples/06b_reuse_multiple_shared_browsers.py
'''
import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import get_browser


class Settings(DefaultSettings):
    webdriver_remote_credentials_path = 'credentials.json'


class DuckDuckKeepOpenTest(unittest.TestCase):
    def test_duckduckgo(self):
        # First argument in context name, that matches dictionary key in credentials.json
        with get_browser('default') as browser:
            browser.get_url('https://duckduckgo.com/')
            with get_browser('firefox') as browser2:
                browser2.get_url('https://firefox.com/')


if __name__ == "__main__":
    register_settings_instance(Settings())
    unittest.main()
