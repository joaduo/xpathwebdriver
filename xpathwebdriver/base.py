# -*- coding: utf-8 -*-
'''
Smoothtest

Copyright (c) 2014, Juju inc.
Copyright (c) 2011-2013, Joaquin G. Duo
'''
import rel_imp; rel_imp.init()
import logging
import re
import os
from .logger import Logger
from .solve_settings import solve_settings, register_settings


class singleton_decorator(object):

    '''
      Singleton pattern decorator.
      There will be only one instance of the decorated class.
      Decorator always returns same instance.
    '''

    def __init__(self, class_):
        self.class_ = class_
        self.instance = None

    def __call__(self, *a, **ad):
        if self.instance is None:
            self.instance = self.class_(*a, **ad)
        return self.instance


class XpathWdBase(object):
    log = Logger('autotest root', color=solve_settings().get('log_color'))

    @property
    def global_settings(self):
        return solve_settings()


module_regex = re.compile(r'^{mod}(?:\.{mod})*$'.format(mod=r'(?:[a-zA-Z_][a-zA-Z_0-9]*)')) 

def is_valid_file(path):
    '''
    Validate if a passed argument is a existing file (used by argsparse)
    or its a python module namespace path (example.foo.bar.baz)
    '''
    # TODO: should it always validate module string?
    abspath = os.path.abspath(path)
    if not (os.path.exists(abspath)
            and os.path.isfile(abspath)
            or module_regex.match(path)):
        logging.warn('File %r does not exist.' % path)
    return path


class CommandMixin(object):
    def _add_common_args(self, parser):
        parser.add_argument(
            '-S',
            '--settings',
            type=is_valid_file,
            help='Specific settings module path.',
            default=None,
            nargs=1)

    def _process_common_args(self, args):
        # Specific settings
        if args.settings:
            register_settings(args.settings.pop())


def smoke_test_module():
    s = XpathWdBase()
    s.log.i(__file__)


if __name__ == "__main__":
    smoke_test_module()
