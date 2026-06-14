# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import time
import unittest
import threading
from contextlib import contextmanager

import bottle
from selenium.webdriver.remote.webdriver import WebDriver

from xpathwebdriver.browser import Browser
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance, solve_settings


class WebUnitTestBase(unittest.TestCase):
    """
    Base class for tests that need an embedded HTTP server.
    Provides methods to serve custom HTML content for testing without external requests.
    """

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
            yield name
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

    def get_duckduckgo_html(self):
        """
        Returns a simple HTML page mimicking duckduckgo's search form.
        """
        return '''
        <form>
          Search:<br>
          <input type="text" name="q" value="">
        </form>
        '''

    def get_google_html(self):
        """
        Returns a simple HTML page mimicking google's search form.
        """
        return '''
        <form>
          Search:<br>
          <input type="text" id="search_form_input_homepage" value="">
        </form>
        '''

    @classmethod
    def setUpClass(cls):
        class Settings(DefaultSettings):
            xpathbrowser_sleep_multiplier = 0.1
            xpathbrowser_sleep_default_time = 0.1
        register_settings_instance(Settings())
        cls.browser = Browser(settings=solve_settings())
        cls._pages_cache = {}
        cls.setup_http_server()
        # wait for the server to be up
        time.sleep(1)

    @classmethod
    def setup_http_server(cls):
        class MyServer(bottle.WSGIRefServer):
            """
            We need to start a server because browser no longer
            support opening local files (security reason)
            """
            def run(self, app):  # pragma: no cover
                from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
                from wsgiref.simple_server import make_server
                import socket
                class FixedHandler(WSGIRequestHandler):
                    quiet = True
                    def address_string(self):  # Prevent reverse DNS lookups please.
                        return self.client_address[0]
                    def log_request(self, *args, **kw):
                        if not self.quiet:
                            return WSGIRequestHandler.log_request(self, *args, **kw)
                handler_cls = self.options.get('handler_class', FixedHandler)
                server_cls = self.options.get('server_class', WSGIServer)
                if ':' in self.host:  # Fix wsgiref for IPv6 addresses.
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
