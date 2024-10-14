import unittest
from xpathwebdriver.webdriver_manager import get_browser
from xpathwebdriver.default_settings import DefaultSettings


class Settings(DefaultSettings):
    """
    You can generally specify your settings file from:
        - command line: eg `xpathshell --settings path/to/xpathwebdriver_settings.py`
        - environment variable XPATHWD_SETTINGS_FILE or XPATHWD_SETTINGS_MODULE 
    Use `xpathshell --settings-help` command for more details.
    """
    webdriver_browser = 'Chrome'
    webdriver_browser_keep_open = False


class DuckDuckKeepOpenTest(unittest.TestCase):
    """
    Use contexts to create and delete browsers
    """
    def test_duckduckgo(self):
        with get_browser() as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill('.//*[@name="q"]', 'xpathwebdriver\n')
            for link in browser.xpath('//a[contains(@data-testid,"result-title-a")]/@href'):
                print(link)
            print(browser.xpath('//a[contains(@href,"github.com/joaduo")]//text()'))
            browser.click('//a[contains(@href,"github.com/joaduo")]')
            browser.sleep(1)
            self.assertTrue(browser.xpath('//a[contains(text(), "README.md")]'))


if __name__ == "__main__":
    from xpathwebdriver.solve_settings import register_settings_instance
    register_settings_instance(Settings())
    unittest.main()
