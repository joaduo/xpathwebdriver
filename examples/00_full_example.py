"""
# Expected output
    https://pypi.org/project/xpathwebdriver/
    https://github.com/joaduo/xpathwebdriver
    https://libraries.io/pypi/xpathwebdriver
    https://www.guru99.com/xpath-selenium.html
    https://www.scientecheasy.com/2019/11/xpath-contains-text.html/
    https://www.dev2qa.com/how-to-select-the-effective-xpath-for-web-element-in-webdriver/
    https://sqa.stackexchange.com/questions/2485/webdriver-find-elements-by-text
    https://www.geeksforgeeks.org/find_element_by_xpath-driver-method-selenium-python/
    https://stackoverflow.com/questions/29772457/webdriver-select-element-that-has-before
    https://www.testingbits.com/selenium/how-to-locate-element-xpath-in-selenium-webdriver/
    ['GitHub - joaduo/', 'xpathwebdriver', ': Python ', 'Xpath', ' ', 'Webdriver', ' ...', "Your browser indicates if you've visited this link", 'https://github.com', '/joaduo/xpathwebdriver']
    .
    ----------------------------------------------------------------------
    Ran 1 test in 8.394s
    
    OK
"""
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
    def test_duckduckgo(self):
        with get_browser() as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill('.//*[@id="search_form_input_homepage"]', 'xpathwebdriver\n')
            for link in browser.xpath('//a[contains(@class,"result__a")]/@href'):
                print(link)
            print(browser.xpath('//a[contains(@href,"github.com/joaduo")]//text()'))
            browser.click('//a[contains(@href,"github.com/joaduo")]')
            browser.sleep(1)
            self.assertTrue(browser.xpath('//a[contains(text(), "README.md")]'))


if __name__ == "__main__":
    from xpathwebdriver.solve_settings import register_settings_instance
    register_settings_instance(Settings())
    unittest.main()
