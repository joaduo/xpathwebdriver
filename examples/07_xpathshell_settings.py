'''
Use this file to specify xpathshell settings
  xpathshell -S examples/07_xpathshell_settings.py
'''
from xpathwebdriver.default_settings import Settings


class Settings(Settings):
    virtual_display_enable = True # If true, put browser in a contained window
    virtual_display_visible = True # Useful only when backend is not xvnc
