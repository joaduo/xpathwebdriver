'''
For running this test you need to first dump credentials.json
Can be done with command:
    xpathshell -d path/to/dumped/credentials.json

NOTE: if you get multiple warning messages like:
    lib/python3.7/site-packages/selenium/webdriver/remote/remote_connection.py:374: ResourceWarning: unclosed <socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('127.0.0.1', 42646), raddr=('127.0.0.1', 54973)>
      return self._request(command_info[0], url, body=data)
    ResourceWarning: Enable tracemalloc to get the object allocation traceback
You can use examples/monkey_patches/remote_connections_warnings.py patch
This is already fixed in the development version of selenium, but still released.
Check
    https://github.com/SeleniumHQ/selenium/issues/6878
    https://github.com/jimevans/selenium/commit/88ecc549edc5731b8cbc3210a5e4e242e1e5807c
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
