# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
from xpathwebdriver.solve_settings import ConfigVar, BaseSettings
import logging


class DefaultSettings(BaseSettings):
    base_url = ConfigVar(
        doc='specifies the root URL string to build other relative URLs upon',
        default=None,
        parser=str)

    # XpathBrowser related settings
    xpathbrowser_sleep_multiplier = ConfigVar(
        doc='Time multiplier factor for browser.sleep() method',
        default=1)
    xpathbrowser_sleep_default_time = ConfigVar(
        doc='Default time in seconds for browser.sleep() method',
        default=1)
    xpathbrowser_max_wait = ConfigVar(
        doc='Maximum time in seconds, per try, for wait_condition',
        default=5)
    xpathbrowser_default_scheme = ConfigVar(
        doc='When resolving a URL without scheme, what scheme (protocol) to default to',
        default='http')
    xpathbrowser_paths_like_html = ConfigVar(
        doc='When using a relative path if starting with "/" means relative to the root of the server.'
            'If set to False, means all paths are appended to base_url no matter what',
        default=True)

    # Virtual display, most options similar to pyvirtualdisplay.Display class:
    # https://pyvirtualdisplay.readthedocs.io/en/latest/#usage
    virtual_display_enabled = ConfigVar(
        doc='If True use virtual display',
        default=False)
    virtual_display_visible = ConfigVar(
        doc='Show the virtual display in the current display (ignored if backend is set)',
        default=False)
    virtual_display_backend = ConfigVar(
        doc="'xvfb', 'xvnc' or 'xephyr', if set then ignores `virtual_display_visible`",
        default=None,
        parser=str)
    virtual_display_backend_kwargs = ConfigVar(
        doc='**kwargs passed to the virtualdisplay backend class.'
        'Useful for passing rfbauth= file location to xvnc',
        default={},
        parser=eval)
    virtual_display_size = ConfigVar(
        doc='Dimensions in pixels of the virtual display',
        default=(800, 600),
        parser=eval)
    virtual_display_keep_open = ConfigVar(
        doc='Keep virtual display open after process finishes. (for debugging purposes)',
        default=False)

    # Webdriver related settings
    webdriver_browser =  ConfigVar(
        doc='Webdriver\'s browser: Firefox, Chrome, PhantomJs, etc...',
        default='Chrome')
    webdriver_browser_keep_open = ConfigVar(
        doc='Keep browser open after process finishes. (for debugging purposes)',
        default=False)
    webdriver_pool_size = ConfigVar(
        doc='The pool size of open Browsers',
        default=1)
    webdriver_browser_kwargs = ConfigVar(
        doc='**kwargs passed to the webrivers browser class',
        default={},
        parser=eval)
    webdriver_firefox_profile = ConfigVar(
        doc="Specify firefox's profile path Eg: '/home/<user>/.mozilla/firefox/4iyhtofy.xpathwebdriver'",
        default=None,
        parser=str)
    webdriver_window_size = ConfigVar(
        doc='Dimensions in pixels of the Browser\'s window',
        default=(800, 600),
        parser=eval)

    #Remote driver related settings
    webdriver_remote_credentials_path = ConfigVar(
        doc='Path to json file containing remote credentials (as dumped by "xpathshell -d path/to/credentials.json")',
        default=None,
        parser=str)

    #Screenhot related settings
    screenshot_level = ConfigVar(
        doc='Similar to text logging level, but for screenshots (WIP)',
        default=logging.INFO,
        parser=str,
        experimental=True)
    screenshot_exceptions_dir = ConfigVar(
        doc='When an exception occurs during a test, where to save screenshots to',
        default='/tmp/', #FIXME
        parser=str,
        experimental=True)
    assert_screenshots_dir = ConfigVar(
        doc='When asserting/comparing an screenshot where to save taken screenshots to',
        default='/tmp/', #FIXME
        parser=str,
        experimental=True)
    assert_screenshots_learning = ConfigVar(
        doc='If True means we take current screenshot as valid for future comparisons',
        default=False,
        experimental=True)
    assert_screenshots_failed_dir = ConfigVar(
        doc='When asserting/comparing an screenshot where to save failing screenshots to',
        default='/tmp/', #FIXME
        parser=str,
        experimental=True)

    log_level_default = ConfigVar(
        doc='Log level of xpathwebdriver messages',
        default=logging.INFO,
        experimental=True)
    
    log_color = ConfigVar(
        doc='If True use colors in logging messages (not working?)',
        default=logging.INFO,
        experimental=True)


# Soon to be deprecated
Settings = DefaultSettings

