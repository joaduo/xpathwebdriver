# -*- coding: utf-8 -*-
'''
Smoothtest

Copyright (c) 2014, Juju inc.
Copyright (c) 2011-2013, Joaquin G. Duo
'''
import rel_imp
from collections import namedtuple
rel_imp.init()
import re
import os
import traceback
from .logger import Logger
from .solve_settings import solve_settings


TestException = namedtuple('TestException', 'msg repr traceback')


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


class SmoothTestBase(object):
    log = Logger('autotest root', color=solve_settings().get('log_color'))

    @property
    def global_settings(self):
        return solve_settings()

    def _path_to_modstr(self, tst):
        tst = tst.replace(os.path.sep, '.')
        tst = re.sub(r'\.(pyc)|(py)$', '', tst).strip('.')
        return tst

    def split_test_path(self, test_path, meth=False):
        test_path = test_path.split('.')
        if meth:
            offset = -2
            module = '.'.join(test_path[:offset])
            class_ = test_path[offset]
            method = test_path[offset + 1]
            return module, class_, method
        else:  # only module+class
            offset = -1
            module = '.'.join(test_path[:offset])
            class_ = test_path[offset]
            return module, class_

    def get_module_file(self, module):
        pth = module.__file__
        if pth.endswith('.pyc'):
            pth = pth[:-1]
        return pth

    def reprex(self, e, print_=True):
        # TODO: shuoldn't format last exception,but passed one
        if print_:
            traceback.print_exc()
        return TestException(str(e), repr(e), traceback.format_exc())


def smoke_test_module():
    s = SmoothTestBase()
    s.log.i(__file__)


if __name__ == "__main__":
    smoke_test_module()
