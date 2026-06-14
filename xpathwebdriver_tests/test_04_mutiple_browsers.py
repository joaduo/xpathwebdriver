import unittest
from xpathwebdriver.webdriver_manager import get_browser
from xpathwebdriver_tests.test_utils import WebUnitTestBase


class DuckDuckTest(WebUnitTestBase):
    def test_duckduckgo(self):
        # Use WebdriverManager for more than 1 browser context
        duckduckgo_body = self.get_duckduckgo_html()
        with self.create_html('duckduckgo', duckduckgo_body) as duckduckgo_path:
            google_body = self.get_google_html()
            with self.create_html('google', google_body) as google_path:
                # Use get_browser with different context names
                with get_browser('First', 'Chrome') as browser:
                    browser.get_url(self._path_to_url(duckduckgo_path))
                    browser.fill(".//*[@name='q']", 'xpathwebdriver\n')
                    with get_browser('Second', 'Chrome') as browser2:
                        browser2.get_url(self._path_to_url(google_path))


if __name__ == "__main__":
    unittest.main()
