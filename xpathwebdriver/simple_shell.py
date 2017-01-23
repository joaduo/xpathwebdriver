# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from argparse import ArgumentParser
from .logger import Logger
from .simple_xpath_browser import SimpleXpathBrowser
from .base import CommandMixin

logger = Logger(color=True)

class ShellXpathBrowser(SimpleXpathBrowser):
    def get_url(self, url, condition=None):
        SimpleXpathBrowser.get_url(self, url, condition=condition)
        self.log.i(" Current url: %s" % self.current_url())

def embed(url):
    """Call this to embed IPython at the current point in your program.
    """
    iptyhon_msg = ('Could not embed Ipython, falling back to ipdb'
                   ' shell. Exception: %r')
    ipdb_msg = ('Could not embed ipdb, falling back to pdb'
                ' shell. Exception: %r')
    b = browser = ShellXpathBrowser(logger=logger)
    if url:
        b.get(url)
    display_banner = ("XpathBrowser in 'b' or 'browser' variables\n"
                      " Current url: %s" % b.current_url())
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        # Now create the IPython shell instance. Put ipshell() anywhere in your code
        # where you want it to open.
        ipshell = InteractiveShellEmbed(banner2=display_banner)
        ipshell()
        del b
        del browser
    except Exception as e:
        logger.w(iptyhon_msg % e)
        try:
            import ipdb
            ipdb.set_trace()
        except Exception as e:
            logger.e(ipdb_msg % e)
            import pdb
            pdb.set_trace()


class XpathShellCommand(CommandMixin):
    def get_parser(self):
        parser = ArgumentParser(description='Test XPaths via Selenium.')
        parser.add_argument('url', nargs='?')
        self._add_common_args(parser)
        return parser

    def main(self, argv=None):
        args = self.get_parser().parse_args(argv)
        self._process_common_args(args)
        embed(args.url)


def smoke_test_module():
    XpathShellCommand()
    b = ShellXpathBrowser()
    b.get('http://localhost')


def main(argv=None):
    XpathShellCommand().main(argv)


if __name__ == "__main__":
    main()

