# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''

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
