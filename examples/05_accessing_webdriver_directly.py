import unittest
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance
from xpathwebdriver.webdriver_manager import WebdriverManager


class Settings(DefaultSettings):
    #Override here any desired option check example 02
    pass


class DuckDuckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register_settings_instance(Settings())

    def test_duckduckgo(self):
        with WebdriverManager().enter_level() as browser:
            driver = browser.get_driver()
            driver.get('https://duckduckgo.com')
            element = driver.find_element_by_id('search_form_input_homepage')
            element.send_keys('Example')
        
            
if __name__ == "__main__":
    unittest.main()
