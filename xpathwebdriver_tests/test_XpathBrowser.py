# -*- coding: utf-8 -*-
'''
xpathwebdriver

Code Licensed under MIT License. See LICENSE file.
'''
import unittest
from selenium.webdriver.remote.webdriver import WebDriver

from xpathwebdriver_tests.test_utils import WebUnitTestBase


class TestXpathBrowser(WebUnitTestBase):
    '''
    TODO:
    - get_url (with condition)
    - get_path (with condition)
    '''
    def test_fill(self):
        body = '''
        <form>
          First name:<br>
          <input id=1 type="text" name="firstname">
          <br>
          Last name:<br>
          <input id=2 type="text" name="lastname">
        </form> 
        '''
        self.browser.set_base_url('http://mepinta.com/')
        self.assertEqual(self.browser.build_url('example'), 'http://mepinta.com/example')
        with self.create_html('test_fill', body) as path:
            self.get_local_page(path)
            self.assertTrue(self.browser.current_path.endswith('test_fill'))
            self.assertTrue(self.browser.current_url.endswith('test_fill'))
            self.assertIsInstance(self.browser.get_driver(), WebDriver)
            self.browser.fill_form(firstname='John1', lastname='Doe1')
            self.browser.fill_form_attr('id', {1:'John2', 2:'Doe2'})
            self.browser.fill_form_ordered([('firstname','John3'), ('lastname','Doe3')])
            self.browser.fill_form_xpath({'//form/input[1]':'John4','//form/input[2]':'Doe4'})
    def test_click(self):
        body = "<button id='example_button'>Example</button>"
        with self.create_html('test_click', body) as path:
            self.get_local_page(path)
            self.browser.click('.//button')
            self.browser.click(".//*[@id='example_button']")
    def test_sleep(self):
        self.browser.sleep()
        self.browser.sleep(0.1)
        self.browser.sleep(0.1, condition='>')
        self.browser.sleep(condition='<')
        self.browser.sleep(0.05, condition='=')
        self.browser.sleep(1, condition='><')
    def test_select(self):
        body = '''
          <div>
              <div id='some_text'>
                <p>The quick fox jumped over the Lorem Ipsum.</p>
              </div>
              <div id='some_other'>
                <p>The other quick fox jumped over the Lorem Ipsum.</p>
              </div>
          </div>
        '''
        with self.create_html('test_select', body) as path:
            self.get_local_page(path)
            self.assertTrue(self.browser.select_xpath('//div'))
            self.assertTrue(self.browser.select_xsingle('//div'))
            found = self.browser.wait_condition(lambda b: b.select_xpath('//div'))
            self.assertTrue(found)
            found = self.browser.wait_condition(lambda b: b.select_xpath('//div/form'), max_wait=0.1)
            self.assertFalse(found)
            # default condition
            found = self.browser.wait_condition()
            self.assertTrue(found)
    def test_window(self):
        body = "<h1>Example</h1>"
        with self.create_html('test_target_window', body) as target:
            body = f"<a href='{self._path_to_url(target)}' target='blank'>Example</a>"
            with self.create_html('test_window', body) as path:
                self.get_local_page(path)
                self.browser.click('.//a')
                with self.browser.window():
                    self.assertTrue(self.browser.xpath('//h1/text()'))


if __name__ == "__main__":
    unittest.main()
