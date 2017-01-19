# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
from selenium.common.exceptions import UnexpectedAlertPresentException
from xpathwebdriver.logger import Logger
from xpathwebdriver.xpath_browser import XpathBrowser
from contextlib import contextmanager
from selenium.webdriver.remote.webdriver import WebDriver
import tempfile
import shutil
import unittest
import os
from xpathwebdriver.webdriver_manager import WebdriverManager
from xpathwebdriver.levels import SINGLE_TEST_LIFE


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
            self._tempdir = tempfile.mkdtemp(prefix='smoothtest')
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

    def setUp(self):
        self.__level_mngr = WebdriverManager().enter_level(level=SINGLE_TEST_LIFE)
        webdriver = self.__level_mngr.acquire_driver()
        logger = Logger(__name__)
        self.browser = XpathBrowser(webdriver, logger=logger, settings={})
        # Temp dir to save pages
        self._tempdir = None

    def tearDown(self):
        self.__level_mngr.exit_level()
        if self._tempdir:
            shutil.rmtree(self._tempdir, ignore_errors=True)
            self._tempdir = None


class TestXpathBrowser(WebUnitTestBase):
    '''
    TODO:
    - test select/has/extract 
    - get_url (with condition)
    - get_path (with condition)
    - test wait
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
            self.assertTrue(self.browser.current_path().endswith('.html'))
            self.assertTrue(self.browser.current_url().endswith('.html'))
            self.assertIsInstance(self.browser.get_driver(), WebDriver)
            self.browser.fill_form(firstname='John1', lastname='Doe1')
            self.browser.fill_form_attr('id', {1:'John2', 2:'Doe2'})
            self.browser.fill_form_ordered([('firstname','John3'), ('lastname','Doe3')])
            self.browser.fill_form_xpath({'//form/input[1]':'John4','//form/input[2]':'Doe4'})

#    def test_wipe_alerts(self):
#        body = '''
#          <script type="text/javascript">
#            alert('Example alert');
#          </script>
#        '''
#        try:
#            with self.create_html('test_wipe_alerts', body) as path:
#                self.get_local_page(path)
#        except UnexpectedAlertPresentException:
#            self.browser.wipe_alerts()
#        else:
#            # Fails on Chrome, since alert blocks page loading
#            self.fail('No alert wiped')

    def test_click(self):
        body = "<button id='example_button'>Example</button>"
        with self.create_html('test_click', body) as path:
            self.get_local_page(path)
            self.browser.click('.//button')
            self.browser.click(".//*[@id='example_button']")
            
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
            self.browser.select_xpath('//div')
            self.browser.select_xsingle('//div')


if __name__ == "__main__":
    unittest.main()
