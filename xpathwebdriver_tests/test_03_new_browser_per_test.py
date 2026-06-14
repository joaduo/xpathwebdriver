import unittest
from xpathwebdriver_tests.test_utils import WebUnitTestBase


class NewBrowserPerTest(WebUnitTestBase):
    def test_duckduckgo(self):
        body = self.get_duckduckgo_html()
        with self.create_html('duckduckgo', body) as path:
            self.get_local_page(path)
            self.browser.fill('.//*[@name="q"]', 'xpathwebdriver\n')

    def test_duckduckgo_rel_imp(self):
        body = self.get_duckduckgo_html()
        with self.create_html('duckduckgo_rel_imp', body) as path:
            self.get_local_page(path)
            self.browser.fill('.//*[@name="q"]', 'rel_imp python\n')


if __name__ == "__main__":
    unittest.main()
