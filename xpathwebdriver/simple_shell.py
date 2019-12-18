# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from argparse import ArgumentParser
from .logger import Logger
from .browser import Browser
from .base import CommandMixin
import json
import os
from xpathwebdriver.default_settings import DefaultSettings
import logging
from xpathwebdriver.solve_settings import solve_settings


logger = Logger(level=logging.DEBUG, color=False)


class ShellBrowser(Browser):
    def get_url(self, url, condition=None):
        Browser.get_url(self, url, condition=condition)
        self.log.i(" Current url: %s" % self.current_url)


def dump_credentials(browser, dump_path, context_name, wipe_credentials):
    logger.info('Dumping webdriver remote credentials to %s', dump_path)
    creds = {}
    if os.path.exists(dump_path) and not wipe_credentials:
        with open(dump_path, 'r') as fp:
            creds = json.load(fp)
    creds[context_name] = browser.get_remote_credentials()
    with open(dump_path, 'w') as fp:
        json.dump(creds, fp)


def embed(args):
    '''
    :param args: parser args object
    '''
    ipython_msg = ('Could not embed Ipython, falling back to ipdb'
                   ' shell. Exception: %r')
    ipdb_msg = ('Could not embed ipdb, falling back to pdb'
                ' shell. Exception: %r')
    b = browser = ShellBrowser(logger=logger)
    if args.dump_credentials:
        dump_credentials(browser, args.dump_credentials, args.context_name, args.wipe_credentials)
    if args.url:
        b.get(args.url)
    display_banner = ("XpathBrowser in 'b' or 'browser' variables\n"
                      " Current url: %s" % b.current_url)
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
        browser._free_webdriver()


class XpathShellCommand(CommandMixin):
    def get_parser(self):
        parser = ArgumentParser(description='Test XPaths via Selenium.')
        parser.add_argument('url', nargs='?')
        parser.add_argument('-p','--print-credentials', action='store_true',
            help='Print remote credentials just after starting.')
        parser.add_argument('-d','--dump-credentials', type=str,
            help='Dump webdriver\'s remote credentials to file.',
            default=None,)
        parser.add_argument('-w','--wipe-credentials', action='store_true',
            help='Empty other credentials in file.')
        parser.add_argument('-c','--context-name', type=str,
            help='When dumping credentials, set this context name.',
            default='default',)
        parser.add_argument('-e','--environment-variables', action='store_true',
            help='Print available environment variables for configuration.')
        parser.add_argument('--settings-help', action='store_true',
            help='Print settings help documentation.')
        self._add_common_args(parser)
        return parser

    def main(self, argv=None):
        args = self.get_parser().parse_args(argv)
        self._process_common_args(args)
        if args.environment_variables:
            self.print_env_vars()
        elif args.settings_help:
            self.print_settings_help()
        else:
            embed(args)

    def print_env_vars(self):
        print('\n# Available environment variables to override configuration (current values if declared): \n')
        for n,cfg in sorted(solve_settings().get_config_vars().items()):
            if cfg.experimental:
                continue
            print('%s=%s\t\t(default:%r)' % (n, cfg.value, cfg.default))

    def print_settings_help(self):
        settings_doc = '''
## Xpathwebdriver Settings Variables
You can declare variables inside a Settings class inherinting from DefaultSettings.
(check examples/02_using_settings_keep_open.py as a reference on how to do it)

You can also export an environment variable to override any configuration.
(check examples/08_settings_use_environment_variables.py)
%s
        '''
        vars_doc = ''
        for env_var,cfg in sorted(solve_settings().get_config_vars().items()):
            dc = '''
* {cfg.name} (python)
  {env_var} (env var)
{experimental}    {cfg.doc}
'''.format(cfg=cfg,
           env_var=env_var,
           experimental=' status:EXPERIMENTAL\n' if cfg.experimental else '')
            vars_doc += dc
        print(settings_doc % vars_doc)


def main(argv=None):
    XpathShellCommand().main(argv)


if __name__ == "__main__":
    main()

