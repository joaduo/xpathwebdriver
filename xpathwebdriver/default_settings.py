# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import logging
import json


class Settings(object):
    def __init__(self):
        if self.webdriver_remote_credentials_path:
            with open(self.webdriver_remote_credentials_path, 'r') as fp:
                cred = json.load(fp)
            self.webdriver_remote_command_executor = cred['webdriver_remote_command_executor']
            self.webdriver_remote_session_id = cred['webdriver_remote_session_id']

    @property
    def base_url(self):
        return self.web_server_url

    # Server to be tested URL eg: http://www.example.com 
    web_server_url = ''

    # Virtual display is useful to keep the webdriver browser contained
    # avoiding the browser to pop-up abover other windows (with alerts for example)
    virtual_display_enable = False # Use virtual display
    virtual_display_visible = False # Show the virtual display or may be hidden (for headless testing)
    virtual_display_backend = None # 'xvfb', 'xvnc' or 'xephyr', ignores ``virtual_display_visible``
    virtual_display_size = (800, 600) # Dimensions of the virtual display
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
    log_level_root_handler = logging.DEBUG
    log_color = False # Not working on Python 3


def smoke_test_module():
    Settings()

if __name__ == "__main__":
    smoke_test_module()
