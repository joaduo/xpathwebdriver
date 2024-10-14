import unittest
from xpathwebdriver.webdriver_manager import get_browser
from xpathwebdriver.solve_settings import solve_settings


class DuckDuckKeepOpenTest(unittest.TestCase):
    def test_remote(self):
        settings = solve_settings()
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')
        settings.set('webdriver_browser_kwargs', dict(options=options, command_executor="http://localhost:4444"))
        with get_browser(browser='Remote') as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill('.//*[@id="search_form_input_homepage"]', 'xpathwebdriver\n')


if __name__ == "__main__":
    from xpathwebdriver.solve_settings import register_settings_instance
    unittest.main()
