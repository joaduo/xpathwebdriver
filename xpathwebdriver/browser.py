# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from .webdriver_manager import WebdriverManager
from .xpath_browser import XpathBrowser
from .solve_settings import register_settings_instance, solve_settings


class Browser(XpathBrowser):
    '''
    Use this class when using only one browser at a time
    and you don't require complex browser leveling.

    For multiple browsers at the same time check examples/04_mutiple_browsers.py
    '''
    def __init__(self, base_url=None, logger=None, settings=None, context_name='default'):
        if settings:
            register_settings_instance(settings)
        else:
            settings = solve_settings()
        self._browser_context = WebdriverManager().get_browser(context_name=context_name)
        XpathBrowser.__init__(self, self._browser_context.acquire_driver(),
                base_url=base_url, logger=logger, settings=settings)

    def __del__(self):
        self._free_webdriver()

    def _free_webdriver(self):
        # We may get an exception before setting _browser_context 
        if getattr(self, '_browser_context', None):
            self._browser_context.__exit__()
            self._browser_context = None

    def _quit_failed_webdriver(self):
        failed = WebdriverManager()._is_failed_webdriver(self.driver)
        if failed:
            self._free_webdriver()
        return failed

