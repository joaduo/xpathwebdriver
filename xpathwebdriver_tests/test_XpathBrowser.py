# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
from contextlib import contextmanager
from selenium.webdriver.remote.webdriver import WebDriver
import tempfile
import shutil
import unittest
import os
from xpathwebdriver.browser import Browser
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance,\
    solve_settings


class WebUnitTestBase(unittest.TestCase):

    def _path_to_url(self, path):
        return 'file://' + path

    def get_local_page(self, path):
        self.browser.get_url(self._path_to_url(path))

    @contextmanager
    def create_html(self, name, body, **kwargs):
        templ = '''
<!DOCTYPE html>
<html>
<head>
  {jquery}
  <title>{name}</title>
</head>
<body>
      {body}
</body>
</html>
        '''
        jquery = ''
        kwargs.update(locals())
        html = templ.format(**kwargs)
        if not self._tempdir:
            self._tempdir = tempfile.mkdtemp(prefix='xpathwebdriver')
        path = os.path.join(self._tempdir, name + '.html')
        # Create html page in temporary dir
        with open(path, 'w') as fh:
            fh.write(html)
        try:
            yield  path
        except:
            raise
        finally:
            os.remove(path)

    @classmethod
    def setUpClass(cls):
        class Settings(DefaultSettings):
            xpathbrowser_sleep_multiplier = 0.1
            xpathbrowser_sleep_default_time = 0.1
        register_settings_instance(Settings())
        cls.browser = Browser(settings=solve_settings())
        cls._tempdir = None

    @classmethod
    def tearDownClass(cls):
        del cls.browser

    def tearDown(self):
        if self._tempdir:
            shutil.rmtree(self._tempdir, ignore_errors=True)
            self._tempdir = None


class TestXpathBrowser(WebUnitTestBase):
    '''
    TODO:
    - test valid_*
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
            self.assertTrue(self.browser.current_path.endswith('.html'))
            self.assertTrue(self.browser.current_url.endswith('.html'))
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


if __name__ == "__main__":
    unittest.main()
