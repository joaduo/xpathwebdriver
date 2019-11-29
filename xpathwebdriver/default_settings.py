# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import logging
import json
import os


logger = logging.getLogger('default_settings')


class ConfigVar(object):
    def __init__(self, value, name=None, parser=None):
        self.value = value
        self.name = name
        self.parser = parser or self._solve_parser()

    def _solve_parser(self, value):
        parser = type(value)
        if parser == bool:
            parser = eval
        return parser

    def parse(self, value_str):
        return self.parser(value_str)


class Settings(object):
    # Server to be tested URL eg: http://www.example.com 
    base_url = None

    xpathbrowser_wait_timeout = 2
    xpathbrowser_default_scheme = 'http'
    xpathbrowser_paths_like_html = True # when using a relative path if starting with "/" means relative to the root of the server
                                        # if set to False, means all paths are appended to _base_url no matter what

    # Virtual display is useful to keep the webdriver browser contained
    # avoiding the browser to pop-up abover other windows (with alerts for example)
    virtual_display_enabled = False # Use virtual display
    virtual_display_visible = False # Show the virtual display or may be hidden (for headless testing)
    virtual_display_backend = ConfigVar(None, parser=str) # 'xvfb', 'xvnc' or 'xephyr', if set then ignores `virtual_display_visible`
    virtual_display_size = ConfigVar((800, 600), parser=eval) # Dimensions of the virtual display
    virtual_display_keep_open = False # If we want to check results (useful whe combined with webdriver_browser_keep_open)

    webdriver_enabled = True # Whether or not automatically create the browser
    webdriver_browser = 'Chrome' # Which browser we would like to use webdriver with: Firefox, Chrome, PhantomJs, etc...
    webdriver_browser_keep_open = False # Keep browser open after python process is dead
    webdriver_pool_size = 1

    #Remote driver/reuse open driver
    webdriver_remote_command_executor = '' # Manually provide the url for the driver eg: 'http://127.0.0.1:54551'
    webdriver_remote_session_id = ''       # Manually provide session id for reusage eg: '4aed25f4a5ce78bb7d57c19663110b3c'
    webdriver_remote_credentials_path = '' # Path to json file containing previous 2 key above (eg:dumped by "xpathshell -d <path>.json")

    #webdriver_browser_life DEPRECATED, never used in code

    # Browsers profiles
    # Eg: '/home/<user>/.mozilla/firefox/4iyhtofy.webdriver_autotest' on linux
    # or: 'C:/Users/<user>/AppData/Roaming/Mozilla/Firefox/Profiles/c1r3g2wi.default' on windows
    webdriver_firefox_profile = None

    screenshot_level = 0 # Like a text logging level, but doing screenshots (WIP) 
                        # Higher level-> more screenshots per action
    screenshot_exceptions_dir = './' # Were to save logged screenshot
    
    assert_screenshots_dir = '/tmp/'
    assert_screenshots_learning = False
    assert_screenshots_failed_dir = '/tmp/'

    log_level_default = logging.INFO
    log_color = False # Not working on Python 3

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


def smoke_test_module():
    Settings()

if __name__ == "__main__":
    smoke_test_module()
