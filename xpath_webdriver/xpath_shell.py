# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from smoothtest.webunittest.WebdriverManager import WebdriverManager
from smoothtest.settings.default import PROCESS_LIFE
import urlparse
from argparse import ArgumentParser
from smoothtest.base import CommandBase
from smoothtest.IpythonEmbedder import IpythonEmbedder
from smoothtest.Logger import Logger

class XpathShell(object):
    def __init__(self, logger=None):
        self.log = logger or Logger('Xpath Shell')

    def get(self, url):
        u = urlparse.urlparse(url)
        if not u.scheme:
            u = ('http', u.netloc, u.path, u.params, u.query, u.fragment)
            url = urlparse.urlunparse(u)
        self.browser.get_url(url)
        self.log.i('Current url: %r' % self.browser.current_url())

    def run_shell(self, url=None):
        self.level_mngr = WebdriverManager().enter_level(level=PROCESS_LIFE)
        browser = self.browser = self.level_mngr.get_xpathbrowser(name='Browser')
        #Aliases #TODO: add ipython extension
        ex  = extract = browser.extract_xpath
        exs = xsingle = browser.extract_xsingle
        get = self.get
        def reset_browser():
            self.level_mngr.exit_level()
            self.level_mngr = WebdriverManager().enter_level(level=PROCESS_LIFE)
        if url:
            self.get(url)
        print('Available objects/commands %s' % sorted(locals()))
        IpythonEmbedder().embed()
        self.level_mngr.exit_level()
        WebdriverManager().stop_display()

class XpathShellCommand(CommandBase):

    def get_parser(self):
        parser = ArgumentParser(description='Test XPaths via Selenium.')
        parser.add_argument('url', nargs='?')
        self._add_smoothtest_common_args(parser)
        return parser

    def main(self, argv=None):
        args = self.get_parser().parse_args(argv)
        url = args.url
        XpathShell().run_shell(url=url)

def smoke_test_module():
    c = XpathShellCommand()

def main(argv=None):
    XpathShellCommand().main(argv)

if __name__ == "__main__":
    main()
