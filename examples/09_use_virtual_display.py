'''
1. Make sure you installed Xephyr
2. You can optionally install vncserver and xvfb (as two other alternatives)
3. Check available settings (grep filters variables starting with "virtual_display")
    xpathshell --settings-help | grep virtual_display -A 3 -B 1
4. Check pyvirtualdisplay documentation at (many of the settings match those of pyvirtualdisplay)
    https://pyvirtualdisplay.readthedocs.io/en/latest/#usage
5. Run this exmaple adding and modifying virtual_display settings
    python3 examples/09_use_virtual_display.py
'''
import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import get_browser


class Settings(DefaultSettings):
    virtual_display_enabled = True
    virtual_display_visible = True #Use Xephyr


class DuckDuckKeepOpenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def test_duckduckgo(self):
        with get_browser() as browser:
            browser.get_url('https://duckduckgo.com/')


if __name__ == "__main__":
    unittest.main()
