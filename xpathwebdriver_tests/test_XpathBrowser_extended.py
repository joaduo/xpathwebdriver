# -*- coding: utf-8 -*-
'''
xpathwebdriver

Code Licensed under MIT License. See LICENSE file.
'''
import unittest
import os
import tempfile
from selenium.webdriver.remote.webdriver import WebDriver

from xpathwebdriver_tests.test_utils import WebUnitTestBase


class TestXpathBrowserExtended(WebUnitTestBase):
    '''
    Extended test suite for XpathBrowser class covering all methods.
    '''
    
    def test_set_base_url(self):
        '''Test setting base URL'''
        self.browser.set_base_url('http://example.com/')
        self.assertEqual(self.browser.base_url, 'http://example.com/')
        self.browser.set_base_url('https://example.com/path/')
        self.assertEqual(self.browser.base_url, 'https://example.com/path/')
    
    def test_build_url(self):
        '''Test building URLs from paths'''
        self.browser.set_base_url('http://example.com/')
        self.assertEqual(self.browser.build_url('/test'), 'http://example.com/test')
        self.assertEqual(self.browser.build_url('test'), 'http://example.com/test')
        self.assertEqual(self.browser.build_url('/test?param=1'), 'http://example.com/test?param=1')
        
    def test_clean_url(self):
        '''Test URL cleaning'''
        # Test with domain
        cleaned = self.browser.clean_url('example.com')
        self.assertIn('http', cleaned)
        
        # Test with full URL
        cleaned = self.browser.clean_url('http://example.com')
        self.assertEqual(cleaned, 'http://example.com')
        
        # Test with https
        cleaned = self.browser.clean_url('https://example.com')
        self.assertEqual(cleaned, 'https://example.com')
    
    def test_properties(self):
        '''Test browser properties'''
        body = "<h1>Test</h1>"
        with self.create_html('test_props', body) as path:
            self.get_local_page(path)
            
            # Test driver property
            self.assertIsInstance(self.browser.driver, WebDriver)
            
            # Test current_url property
            self.assertIn('test_props', self.browser.current_url)
            
            # Test current_path property
            self.assertIn('test_props', self.browser.current_path)
            
            # Test get_driver method
            self.assertIsInstance(self.browser.get_driver(), WebDriver)
    
    def test_get_url_with_condition(self):
        '''Test get_url with condition parameter'''
        body = "<h1>Loaded</h1>"
        with self.create_html('test_get_url_cond', body) as path:
            url = self._path_to_url(path)
            # Test with javascript condition
            condition = 'return document.querySelector("h1") !== null;'
            self.browser.get_url(url, condition)
            self.assertIn('test_get_url_cond', self.browser.current_url)
    
    def test_get_page(self):
        '''Test get_page method'''
        self.browser.set_base_url(f'http://{self.host}:{self.port}/')
        body = "<h1>Page Test</h1>"
        with self.create_html('test_get_page', body) as path:
            self.browser.get_page(path)
            self.assertIn('test_get_page', self.browser.current_url)
    
    def test_get_page_once(self):
        '''Test get_page_once method - should not reload if already on page'''
        self.browser.set_base_url(f'http://{self.host}:{self.port}/')
        body = "<h1>Once Test</h1>"
        with self.create_html('test_get_page_once', body) as path:
            # First load
            self.browser.get_page_once(path)
            url_after_first = self.browser.current_url
            
            # Second call - should not reload
            self.browser.get_page_once(path)
            url_after_second = self.browser.current_url
            
            self.assertEqual(url_after_first, url_after_second)
    
    def test_xpath_variations(self):
        '''Test xpath method with different parameters'''
        body = '''
        <div>
            <span class="item">Item 1</span>
            <span class="item">Item 2</span>
            <span class="item">Item 3</span>
        </div>
        '''
        with self.create_html('test_xpath_var', body) as path:
            self.get_local_page(path)
            
            # Test xpath with single=False (default)
            items = self.browser.xpath('//span[@class="item"]')
            self.assertEqual(len(items), 3)
            
            # Test xpath with single=True
            first_item = self.browser.xpath('//span[@class="item"]', single=True)
            self.assertIsNotNone(first_item)
            
            # Test xpath for text
            text = self.browser.xpath('//span[@class="item"]/text()', single=True)
            self.assertIn('Item', text)
    
    def test_css_selectors(self):
        '''Test CSS selector methods'''
        body = '''
        <div>
            <p class="text">Paragraph 1</p>
            <p class="text">Paragraph 2</p>
            <div id="unique">Unique</div>
        </div>
        '''
        with self.create_html('test_css', body) as path:
            self.get_local_page(path)
            
            # Test css method
            items = self.browser.css('.text')
            self.assertEqual(len(items), 2)
            
            # Test select_css (alias)
            items = self.browser.select_css('.text')
            self.assertEqual(len(items), 2)
            
            # Test select_css_single
            unique = self.browser.select_css_single('#unique')
            self.assertIsNotNone(unique)
    
    def test_fill_variations(self):
        '''Test fill method with different parameters'''
        body = '''
        <form>
            <input id="input1" type="text" value="">
            <input id="input2" type="text" value="default">
        </form>
        '''
        with self.create_html('test_fill_var', body) as path:
            self.get_local_page(path)
            
            # Test fill with clear=True
            self.browser.fill('//input[@id="input1"]', 'test1', clear=True)
            
            # Test fill with clear=False
            self.browser.fill('//input[@id="input2"]', 'test2', clear=False)
            
            # Test fill with javascript_safe=True
            self.browser.fill('//input[@id="input1"]', 'test3', clear=True, javascript_safe=True)
    
    def test_execute_script(self):
        '''Test execute_script method'''
        body = "<h1>Script Test</h1>"
        with self.create_html('test_script', body) as path:
            self.get_local_page(path)
            
            # Test script that returns a value
            title = self.browser.execute_script('return document.title;')
            self.assertIn('test_script', title)
            
            # Test script that modifies DOM
            self.browser.execute_script('document.body.style.backgroundColor = "red";')
            
            # Test script with arguments
            result = self.browser.execute_script('return arguments[0] + arguments[1];', 5, 3)
            self.assertEqual(result, 8)
    
    def test_wait_xpath(self):
        '''Test wait_xpath method'''
        body = '''
        <div>
            <span id="delayed" style="display:none">Delayed</span>
        </div>
        '''
        with self.create_html('test_wait_xpath', body) as path:
            self.get_local_page(path)
            
            # Test wait for existing element
            result = self.browser.wait_xpath('//div')
            self.assertTrue(result)
            
            # Test wait for non-existing element with short timeout
            result = self.browser.wait_xpath('//nonexistent', max_wait=0.1)
            self.assertFalse(result)
    
    def test_iframe_context(self):
        '''Test iframe context manager'''
        body = '''
        <iframe id="test_frame" srcdoc="<html><body><h1>Inside Frame</h1></body></html>"></iframe>
        '''
        with self.create_html('test_iframe', body) as path:
            self.get_local_page(path)
            
            # Test iframe context manager
            with self.browser.iframe('//iframe[@id="test_frame"]'):
                # Inside iframe
                self.assertIsNotNone(self.browser.xpath('//h1'))
    
    def test_window_comprehensive(self):
        '''Test window context manager with various parameters'''
        body = "<h1>Target Window</h1>"
        with self.create_html('test_target_win', body) as target:
            body = f"<a href='{self._path_to_url(target)}' target='blank'>Open</a>"
            with self.create_html('test_window_comp', body) as path:
                self.get_local_page(path)
                
                # Test with default parameters
                self.browser.click('.//a')
                with self.browser.window():
                    self.assertIsNotNone(self.browser.xpath('//h1'))
    
    def test_get_selector(self):
        '''Test get_selector method'''
        body = "<div class='test'><span>Content</span></div>"
        with self.create_html('test_selector', body) as path:
            self.get_local_page(path)
            
            element = self.browser.select_xsingle('//div[@class="test"]')
            selector = self.browser.get_selector(element)
            self.assertIsNotNone(selector)
    
    def test_screenshot_methods(self):
        '''Test screenshot methods'''
        body = "<h1>Screenshot Test</h1>"
        with self.create_html('test_screenshot', body) as path:
            self.get_local_page(path)
            
            # Test quick_screenshot
            self.browser.quick_screenshot()
            self.assertTrue(os.path.exists('001.quick_screenshot.png'))
            os.remove('001.quick_screenshot.png')
            
            # Test quick_screenshot with custom path
            with tempfile.TemporaryDirectory() as tmpdir:
                self.browser.quick_screenshot(to_path=tmpdir)
                screenshot_path = os.path.join(tmpdir, '002.quick_screenshot.png')
                self.assertTrue(os.path.exists(screenshot_path))
            
            # Test save_screenshot
            with tempfile.TemporaryDirectory() as tmpdir:
                screenshot_path = os.path.join(tmpdir, 'test_screenshot.png')
                self.browser.save_screenshot(screenshot_path)
                self.assertTrue(os.path.exists(screenshot_path))
    
    def test_wipe_alerts(self):
        '''Test wipe_alerts method'''
        body = """
        <button onclick="alert('Test Alert')">Show Alert</button>
        """
        with self.create_html('test_alerts', body) as path:
            self.get_local_page(path)
            
            # Should not raise exception even if no alert is present
            self.browser.wipe_alerts()
            
            # Note: Testing actual alert dismissal would require triggering an alert
            # which may be flaky in automated tests
    
    def test_get_remote_credentials(self):
        '''Test get_remote_credentials method'''
        # This method is for remote webdriver connections
        # For local testing, it should raise ValueError or return credentials
        try:
            creds = self.browser.get_remote_credentials()
            # If it succeeds, check structure
            self.assertIn('command_executor', creds)
            self.assertIn('session_id', creds)
        except ValueError:
            # Expected for local webdriver
            pass


if __name__ == "__main__":
    unittest.main()
