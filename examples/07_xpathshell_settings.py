'''
Use this file to specify xpathshell settings
  xpathshell -S examples/07_xpathshell_settings.py
'''
from xpathwebdriver.default_settings import Settings


class Settings(Settings):
    virtual_display_enable = True # If true, put browser in a contained window
    #virtual_display_backend = 'xvnc' # If you want to run in a remote server
    virtual_display_size = (800, 600)
    virtual_display_visible = True # Useful only when backend is not xvnc
    virtual_display_keep_open = True # If we want to check results (useful whe combined with webdriver_browser_keep_open)

    webdriver_browser = 'Chrome'
    webdriver_browser_keep_open = True #Survive or not after finishing
