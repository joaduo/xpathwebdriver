# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from .webdriver_manager import WebdriverManager
from .xpath_browser import XpathBrowser


class SimpleXpathBrowser(XpathBrowser):
    def __init__(self, base_url=None, logger=None, settings=None, level=None):
        self._browser_context = WebdriverManager().enter_level(level=level)
        XpathBrowser.__init__(self, self._browser_context.acquire_driver(),
                base_url=base_url, logger=logger, settings=settings)

    def __del__(self):
        if hasattr(self, '_browser_context'):
            self._browser_context.__exit__()


def smoke_test_module():
    xb = SimpleXpathBrowser()
#    import ipdb; ipdb.set_trace()
    xb.get('www.google.com')
#    import ipdb; ipdb.set_trace()

#    print Url
    #xb.get_page_once('www.google.com')
#    xb.get_url('www.google.com')
#    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    smoke_test_module()
