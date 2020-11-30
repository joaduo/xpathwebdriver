import unittest
from xpathwebdriver.webdriver_manager import get_browser


class DuckDuckTest(unittest.TestCase):
    def test_duckduckgo(self):
        with get_browser() as browser:
            driver = browser.driver
            driver.get('https://duckduckgo.com')
            element = driver.find_element_by_id('search_form_input_homepage')
            element.send_keys('Example')
        
            
if __name__ == "__main__":
    unittest.main()
