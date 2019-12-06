'''
Use this file to specify xpathshell settings
  xpathshell -S examples/07_xpathshell_settings.py
'''
from xpathwebdriver.default_settings import DefaultSettings


class Settings(DefaultSettings):
    # Check more details inspecting the DefaultSettings class
    # https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/default_settings.py#L12
    webdriver_browser = 'Firefox'

    # Also check pyvirtualdisplay options
    virtual_display_enabled = True # Use a pyvirtualdisplay
    virtual_display_visible = True # use Xephyr (X server inside window)
