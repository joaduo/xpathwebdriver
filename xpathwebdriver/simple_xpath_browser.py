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


class SimpleXpathBrowser(XpathBrowser):
    '''
    Use this class when using only one browser at a time
    and you don't require complex browser leveling.

    In the context of several test you probably prefer a context manager.
    That way you will save te overhead of creatin a new browser each time.
    Check examples using unit test setup/setupClass teardDown/tearDownClass.
    '''
    def __init__(self, base_url=None, logger=None, settings=None, level=None):
        register_settings_instance(settings)
        self._browser_context = WebdriverManager().enter_level(level=level)
        XpathBrowser.__init__(self, self._browser_context.acquire_driver(),
                base_url=base_url, logger=logger, settings=settings)

    def __del__(self):
        if hasattr(self, '_browser_context'):
            self._browser_context.__exit__()


def smoke_test_module():
    xb = SimpleXpathBrowser()
    xb.get('www.google.com')


if __name__ == "__main__":
    smoke_test_module()
