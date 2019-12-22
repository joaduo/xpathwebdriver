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
import os


logger = logging.getLogger('solve_settings')


class ConfigVar(object):
    def __init__(self, doc=None, default=None, parser=None, experimental=False, env_var=None):
        self.value = default
        self.default = default
        self.parser = parser or self._solve_parser()
        self.name = None
        self.doc = doc
        self.experimental = experimental
        self._env_var = env_var

    @property
    def env_var(self):
        return self._env_var or 'XPATHWD_' + self.name.upper()

    def _solve_parser(self):
        parser = type(self.default)
        if parser == bool:
            parser = eval
        return parser

    def parse(self, value_str):
        return self.parser(value_str)

    def copy(self, value):
        new_cfg = ConfigVar(self.doc, self.default, self.parser, self.experimental, self._env_var)
        new_cfg.name = self.name
        new_cfg.value = value
        return new_cfg


class BaseSettings(object):
    def __init__(self):
        self._load_env_vars()

    def _load_env_vars(self):
        '''
        Support loading from environment variables
        '''
        config_vars = self._get_config_vars()
        self._wrap_raw_values(config_vars)
        for env_var, cfg_var in config_vars.items():
            if env_var in os.environ:
                logger.debug('Using %s=%r => %s', env_var, os.environ[env_var], cfg_var.name)
                setattr(self, cfg_var.name, cfg_var.copy(cfg_var.parse(os.environ[env_var])))

    def _wrap_raw_values(self, config_vars):
        for cfg in config_vars.values():
            name = cfg.name
            if hasattr(self, name):
                value = getattr(self, name)
                if not isinstance(value, ConfigVar):
                    setattr(self, name, cfg.copy(value))

    def _get_config_vars(self):
        config = {}
        for n in dir(self):
            if n.startswith('_'):
                continue
            cfg_var = getattr(self, n)
            if not isinstance(cfg_var, ConfigVar):
                cfg_var = self._solve_config_var(n)
                if not isinstance(cfg_var, ConfigVar):
                    logger.warning('Config variable %r not supported (mispelled/deprecated?)', n)
                    continue
            cfg_var.name = cfg_var.name or n
            config[cfg_var.env_var] = cfg_var
        return config

    @classmethod
    def _solve_config_var(cls, attr):
        cfg_var = getattr(cls, attr, None)
        if (not isinstance(cfg_var, ConfigVar)
        and issubclass(cls.__bases__[0], BaseSettings)):
            return cls.__bases__[0]._solve_config_var(attr)
        return cfg_var


class SettingsWrapper(object):
    '''
    Provide the .get(name, default=None) method for accessing an object's
    attributes.
    Useful for configuration.
    '''
    def __init__(self, settings):
        self._settings = settings

    def get_config_vars(self):
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
    global global_settings
    if not settings:
        logging.debug('Provided empty settings %s', settings)
        return
    if settings == global_settings:
        logging.debug('Settings %s already registered', settings)
        return
    if global_settings:
        logging.debug('Replacing existing settings %r (old) with %r (new)', global_settings, settings)
    if not isinstance(settings, SettingsWrapper):
        settings = SettingsWrapper(settings)
    global_settings = settings


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
