'''
Use this file to specify xpathshell settings
Override this file's configured browser with Firefox
  export XPATHWD_WEBDRIVER_BROWSER="Firefox" && xpathshell -S examples/08_settings_use_environment_variables.py
'''
from xpathwebdriver.default_settings import DefaultSettings


class Settings(DefaultSettings):
    webdriver_browser = 'Chrome'
