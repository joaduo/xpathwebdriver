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
from .Logger import Logger
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


#def get_module_regex():
#    def rpl(str_, local_vars):
#        # replace locals vars in the string
#        return str_.format(**local_vars)
#    mod = r'(?:[a-zA-Z_][a-zA-Z_0-9]*)'
#    mod_path = rpl(r'^{mod}(?:\.{mod})*$', locals())
#    return mod_path
#
#
#def is_valid_file(path):
#    '''
#    Validate if a passed argument is a existing file (used by argsparse)
#    or its a python module namespace path (example.foo.bar.baz)
#    '''
#    # TODO: should it always validate module string?
#    abspath = os.path.abspath(path)
#    if not (os.path.exists(abspath)
#            and os.path.isfile(abspath)
#            or re.match(get_module_regex(), path)):
#        logging.warn('File %r does not exist.' % path)
#    return path
#
#
#def is_file_or_dir(path):
#    '''
#    Validate if a passed argument is a existing file (used by argsparse)
#    '''
#    # TODO: should it always validate module string?
#    abspath = os.path.abspath(path)
#    if not (os.path.exists(abspath)
#            and (os.path.isfile(abspath) or os.path.isdir(abspath))
#            or re.match(get_module_regex(), path)
#            ):
#        logging.warn('File or dir %r does not exist.' % path)
#    return path


#class CommandBase(SmoothTestBase):
#
#    def _add_smoothtest_common_args(self, parser):
#        parser.add_argument(
#            '-S',
#            '--smoothtest-settings',
#            type=is_valid_file,
#            help='Specific smoothtest_settings module path '
#            '(useful if smoothtest_settings module is not in PYTHONPATH).',
#            default=None,
#            nargs=1)
#
#    def _process_common_args(self, args):
#        # Specific settings
#        if args.smoothtest_settings:
#            register_settings(args.smoothtest_settings.pop())
#
#
#class TestRunnerBase(object):
#
#    def __init_values(self):
#        if not hasattr(self, '_already_setup'):
#            self._already_setup = {}
#
#    def _setup_process(self, test, test_path, argv):
#        self.__init_values()
#        if (hasattr(test, 'setUpProcess')
#                and test_path not in self._already_setup):
#            test.setUpProcess(argv)
#            self._already_setup[test_path] = (test, argv)
#
#    def _tear_down_process(self):
#        self.__init_values()
#        for test, argv in self._already_setup.values():
#            if hasattr(test, 'tearDownProcess'):
#                self.log.d('Tearing down process for %r' % test)
#                test.tearDownProcess(argv)
#        self._already_setup.clear()


def smoke_test_module():
    s = SmoothTestBase()
    s.log.i(__file__)
#    trb = TestRunnerBase()
#    trb._setup_process(None, 'path.to.test', [])
#    trb._tear_down_process()


if __name__ == "__main__":
    smoke_test_module()
