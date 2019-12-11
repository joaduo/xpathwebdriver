# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from argparse import ArgumentParser, FileType
from .logger import Logger
from .browser import Browser
from .base import CommandMixin
from .solve_settings import solve_settings
import json
import os


logger = Logger(color=True)


class ShellBrowser(Browser):
    def get_url(self, url, condition=None):
        Browser.get_url(self, url, condition=condition)
        self.log.i(" Current url: %s" % self.current_url())


def dump_credentials(browser, dump_file):
    logger.info('Dumping webdriver remote credentials to %s', dump_file)
    json.dump(browser.get_remote_credentials(), dump_file)
    dump_file.close()


def embed(args):
    """Call this to embed IPython at the current point in your program.
    """
    ipython_msg = ('Could not embed Ipython, falling back to ipdb'
                   ' shell. Exception: %r')
    ipdb_msg = ('Could not embed ipdb, falling back to pdb'
                ' shell. Exception: %r')
    if args.environment_variables:
        print('\n# Available environment variables to override configuration (current values if declared): \n')
        for n in sorted(solve_settings()._get_config_vars().keys()):
            print('%s=%s' % (n, os.environ.get(n,'')))
        print()
        return
    b = browser = ShellBrowser(logger=logger)
    if args.dump_credentials:
        dump_credentials(browser, args.dump_credentials)
    if args.url:
        b.get(args.url)
    display_banner = ("XpathBrowser in 'b' or 'browser' variables\n"
                      " Current url: %s" % b.current_url())
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        # Now create the IPython shell instance. Put ipshell() anywhere in your code
        # where you want it to open.
        ipshell = InteractiveShellEmbed(banner2=display_banner)
        ipshell()
    except Exception as e:
        logger.w(ipython_msg % e)
        try:
            import ipdb
            ipdb.set_trace()
        except Exception as e:
            logger.e(ipdb_msg % e)
            import pdb
            pdb.set_trace()
    finally:
        del browser, b


class XpathShellCommand(CommandMixin):
    def get_parser(self):
        parser = ArgumentParser(description='Test XPaths via Selenium.')
        parser.add_argument('url', nargs='?')
        parser.add_argument('-p','--print-credentials', action='store_true',
            help='Print remote credentials just after starting.')
        parser.add_argument('-d','--dump-credentials', type=FileType('w'),
            help='Dump credentials to file.',
            default=None,)
        parser.add_argument('-e','--environment-variables', action='store_true',
            help='Print available environment variables for configuration.')
        self._add_common_args(parser)
        return parser

    def main(self, argv=None):
        args = self.get_parser().parse_args(argv)
        self._process_common_args(args)
        embed(args)


def main(argv=None):
    XpathShellCommand().main(argv)


if __name__ == "__main__":
    main()

