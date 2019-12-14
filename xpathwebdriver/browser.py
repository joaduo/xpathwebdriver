# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from .webdriver_manager import WebdriverManager
from .xpath_browser import XpathBrowser
from .solve_settings import register_settings_instance


class Browser(XpathBrowser):
    '''
    Use this class when using only one browser at a time
    and you don't require complex browser leveling.

    In the context of several test you probably prefer a context manager.
    That way you will save the overhead of creating a new browser each time.
    Check examples using unit test setup/setupClass teardDown/tearDownClass.
    '''
    def __init__(self, base_url=None, logger=None, settings=None, level=None):
        register_settings_instance(settings)
        self._browser_context = WebdriverManager().enter_level(level=level)
        XpathBrowser.__init__(self, self._browser_context.acquire_driver(),
                base_url=base_url, logger=logger, settings=settings)

    def __del__(self):
        self._free_webdriver()

    def _free_webdriver(self):
        if getattr(self, '_browser_context'):
            self._browser_context.__exit__()
            self._browser_context = None


def smoke_test_module():
    xb = Browser()
    xb.get('duckduckgo.com')


if __name__ == "__main__":
    smoke_test_module()
