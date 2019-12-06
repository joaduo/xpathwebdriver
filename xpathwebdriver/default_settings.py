# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
from xpathwebdriver.solve_settings import ConfigVar, BaseSettings
import logging


class Settings(BaseSettings):
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
