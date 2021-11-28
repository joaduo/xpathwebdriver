# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import unittest
import threading
from contextlib import contextmanager

import bottle
from selenium.webdriver.remote.webdriver import WebDriver

from xpathwebdriver.browser import Browser
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance,\
    solve_settings


class WebUnitTestBase(unittest.TestCase):

    port = 8080
    host = 'localhost'
    @classmethod
    def _path_to_url(cls, path):
        return f'http://{cls.host}:{cls.port}/{path}'

    @classmethod
    def get_local_page(cls, path):
        cls.browser.get_url(cls._path_to_url(path))

    @contextmanager
    def create_html(self, name, body, **kwargs):
        try:
            self.push_page(name, body, **kwargs)
            yield  name
        except:
            raise
        finally:
            self.pop_page(name)

    def push_page(self, name, body, **kwargs):
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
        tmpl_vars = locals().copy()
        tmpl_vars.update(kwargs)
        self._pages_cache[name] = templ.format(**tmpl_vars)

    def pop_page(self, name):
        return self._pages_cache.pop(name)

    @classmethod
    def setUpClass(cls):
        class Settings(DefaultSettings):
            xpathbrowser_sleep_multiplier = 0.1
            xpathbrowser_sleep_default_time = 0.1
        register_settings_instance(Settings())
        cls.browser = Browser(settings=solve_settings())
        cls._pages_cache = {}
        cls.setup_http_server()

    @classmethod
    def setup_http_server(cls):
        class MyServer(bottle.WSGIRefServer):
            def run(self, app): # pragma: no cover
                from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
                from wsgiref.simple_server import make_server
                import socket
                class FixedHandler(WSGIRequestHandler):
                    def address_string(self): # Prevent reverse DNS lookups please.
                        return self.client_address[0]
                    def log_request(*args, **kw):
                        if not self.quiet:
                            return WSGIRequestHandler.log_request(*args, **kw)
                handler_cls = self.options.get('handler_class', FixedHandler)
                server_cls  = self.options.get('server_class', WSGIServer)
                if ':' in self.host: # Fix wsgiref for IPv6 addresses.
                    if getattr(server_cls, 'address_family') == socket.AF_INET:
                        class server_cls(server_cls):
                            address_family = socket.AF_INET6
                srv = make_server(self.host, self.port, app, server_cls, handler_cls)
                ### save tcp server so we can shut it down later
                cls._tcp_server = srv
                srv.serve_forever()
        @bottle.route('/<name>')
        def index(name):
            if name == 'kill':
                raise SystemExit()
            if name in cls._pages_cache:
                return bottle.template(cls._pages_cache[name])
            return None

        kwargs = dict(server=MyServer, host=cls.host, port=cls.port)
        thread = threading.Thread(target=bottle.run, kwargs=kwargs)
        thread.start()
        cls._server_thread = thread

    @classmethod
    def tearDownClass(cls):
        del cls.browser
        cls._tcp_server.shutdown()


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
