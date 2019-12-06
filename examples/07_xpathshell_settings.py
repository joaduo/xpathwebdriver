'''
Use this file to specify xpathshell settings
  xpathshell -S examples/07_xpathshell_settings.py
'''
from xpathwebdriver.default_settings import DefaultSettings


class Settings(DefaultSettings):
    #Override here any desired option
    # Check more details inspecting the DefaultSettings class
    # https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/default_settings.py#L12
    virtual_display_enabled = True # If true, put browser in a contained window
    virtual_display_visible = True # Useful only when backend is not xvnc
