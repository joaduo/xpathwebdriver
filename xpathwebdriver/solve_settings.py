# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import imp

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


global_settings = None
def register_settings(settings_path):
    '''
    Register settings given specific module path.
    :param settings_path:
    '''
    # TODO:Py3
    # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    mod = imp.load_source('specific_smoothtest_settings', settings_path)
    global global_settings
    global_settings = SettingsWrapper(mod.Settings())
    # Set the level of the root logger
    # import here due chicke-egg problem
    from .base import SmoothTestBase
    from .logger import Logger
    Logger.default_level = global_settings.get('log_level_default')
    SmoothTestBase.log.setLevel(global_settings.get('log_level_default'))


def solve_settings():
    '''
    Main function for getting smoothtest global settings.
    #TODO: this goes against any Encapsulated Environment Pattern (context)
    '''
    global global_settings
    if global_settings:
        return global_settings
    else:
        try:
            from xpathwebdriver_settings import Settings
        except ImportError:
            from xpathwebdriver.default_settings import DefaultSettings as Settings
        global_settings = SettingsWrapper(Settings())
        return global_settings


def smoke_test_module():
    print solve_settings()

if __name__ == "__main__":
    smoke_test_module()
