# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
import imp
import importlib
import logging
import json
import os


logger = logging.getLogger('solve_settings')


class ConfigVar(object):
    def __init__(self, value, name=None, parser=None):
        self.value = value
        self.name = name
        self.parser = parser or self._solve_parser(value)

    def _solve_parser(self, value):
        parser = type(value)
        if parser == bool:
            parser = eval
        return parser

    def parse(self, value_str):
        return self.parser(value_str)


class BaseSettings(object):
    def __init__(self):
        self._load_env_vars()
        if self.webdriver_remote_credentials_path:
            with open(self.webdriver_remote_credentials_path, 'r') as fp:
                cred = json.load(fp)
            self._set_and_warn(self.webdriver_remote_credentials_path, 'webdriver_remote_command_executor', cred)
            self._set_and_warn(self.webdriver_remote_credentials_path, 'webdriver_remote_session_id', cred)

    def _set_and_warn(self, path, attr, values):
        if getattr(self, attr):
            logger.warning('Replacing value for %s with values in file %s', attr, path)
        setattr(self, attr, values[attr])

    def _load_env_vars(self):
        '''
        Support loading from environment variables
        '''
        config_vars = self._get_config_vars()
        for env_var, cfg_var in config_vars.items():
            if env_var in os.environ:
                logger.debug('Using %s=%r => %s', env_var, os.environ[env_var], cfg_var.name)
                setattr(self, cfg_var.name, cfg_var.parse(os.environ[env_var]))

    def _get_config_vars(self):
        config = {}
        for n in dir(self):
            if n.startswith('_'):
                continue
            cfg_var = getattr(self, n)
            if not isinstance(cfg_var, ConfigVar):
                cfg_var = ConfigVar(cfg_var)
            cfg_var.name = cfg_var.name or n
            config['XPATHWD_' + n.upper()] = cfg_var
        return config



class SettingsWrapper(object):
    '''
    Provide the .get(name, default=None) method for accessing an object's
    attributes.
    Useful for configuration.
    '''
    def __init__(self, settings):
        self._settings = settings

    def _get_config_vars(self):
        return self._settings._get_config_vars()

    def get(self, name, default=None):
        if hasattr(self._settings, name):
            value = getattr(self._settings, name)
            value = value.value if isinstance(value, ConfigVar) else value
            return value
        return default

    def set(self, name, value):
        setattr(self._settings, name, value)


def register_settings(settings_path):
    '''
    Register settings given specific module path.
    :param settings_path:
    '''
    if isinstance(settings_path, str):
        # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        mod = imp.load_source('specific_xpathwebdriver_settings', settings_path)
        _register_settings_module(mod)
    else:
        register_settings_instance(settings_path)
    set_log_level()


def _register_settings_module(mod):
    if hasattr(mod, 'Settings'):
        settings_cls = mod.Settings
    else:
        settings_cls = mod.DefaultSettings
    register_settings_instance(settings_cls())


global_settings = None
def register_settings_instance(settings):
    if not settings:
        logging.debug('Provided settings object evals to False', settings)
        return
    global global_settings
    if global_settings:
        logging.debug('Replacing existing settings %r (old) with %r (new)', global_settings, settings)
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
    Main function for getting xpathwebdrivertest global settings.
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
