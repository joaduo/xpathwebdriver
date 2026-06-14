import unittest
from xpathwebdriver_tests.test_utils import WebUnitTestBase


class DuckDuckBasic(WebUnitTestBase):
    """
    In this example we show how use setup and tearDown methods.
    If for some reason we want to avoid context manager as used in 00_full_example.py

    Note: We use the class-level browser created in setUpClass.
    """
    def test_duckduckgo(self):
        body = self.get_duckduckgo_html()
        with self.create_html('duckduckgo', body) as path:
            self.get_local_page(path)
            # Type xpathwebdriver and press enter
            self.browser.fill('.//*[@name="q"]', 'xpathwebdriver\n')

    def test_duckduckgo_rel_imp(self):
        body = self.get_duckduckgo_html()
        with self.create_html('duckduckgo_rel_imp', body) as path:
            self.get_local_page(path)
            self.browser.fill('.//*[@name="q"]', 'rel_imp python\n')


if __name__ == "__main__":
    unittest.main()
