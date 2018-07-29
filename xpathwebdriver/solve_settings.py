# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
import imp
import importlib


# TODO: support .cfg files
class SettingsWrapper(object):
    '''
    Provide the .get(name, default=None) method for accessing an object's
    attributes.
    Useful for configuration.
    '''
    def __init__(self, settings):
        self._settings = settings

    def get(self, name, default=None):
        if hasattr(self._settings, name):
            return getattr(self._settings, name)
        return default

    def set(self, name, value):
        setattr(self._settings, name, value)


def register_settings(settings_path):
    '''
    Register settings given specific module path.
    :param settings_path:
    '''
    if isinstance(settings_path, str):
        # TODO:Py3
        # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        mod = imp.load_source('specific_smoothtest_settings', settings_path)
        _register_settings_module(mod)
    else:
        _register_settings_instance(settings_path)
    set_log_level()


def _register_settings_module(mod):
    _register_settings_instance(mod.Settings())


global_settings = None
def _register_settings_instance(settings):
    global global_settings
    global_settings = SettingsWrapper(settings)


def set_log_level():
    # Set the level of the root logger
    # import here due chicke-egg problem
    from .base import XpathWdBase
    from .logger import Logger
    _set_log_level(XpathWdBase, Logger)


def _set_log_level(base_cls, logger_cls):
    logger_cls.default_level = global_settings.get('log_level_default')
    base_cls.log.setLevel(global_settings.get('log_level_default'))


def solve_settings():
    return _solve_settings('xpathwebdriver.default_settings')


def _solve_settings(default_mod):
    '''
    Main function for getting smoothtest global settings.
    #TODO: this goes against any Encapsulated Environment Pattern (context)
    '''
    global global_settings
    if not global_settings:
        _register_settings_module(importlib.import_module(default_mod))
    return global_settings


def smoke_test_module():
    from .logger import log_test
    global called_once
    called_once = True
    log_test(solve_settings())
    #set_log_level()


if __name__ == "__main__":
    smoke_test_module()
