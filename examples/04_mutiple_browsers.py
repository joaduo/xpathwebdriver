import unittest
from xpathwebdriver.webdriver_manager import get_browser


class DuckDuckTest(unittest.TestCase):
    def test_duckduckgo(self):
        #Use WebdriverManager for more than 1 browser
        with get_browser('First', 'Chrome') as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
            with get_browser('Second', 'Firefox') as browser2:
                browser2.get_url('https://google.com/')


if __name__ == "__main__":
    unittest.main()
