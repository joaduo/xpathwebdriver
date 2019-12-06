'''
Use this file to specify xpathshell settings
  xpathshell -S examples/07_xpathshell_settings.py
You need to have vnc server installed (so the Xvnc command is available)
Check pyvirtualdisplay for details
Set your vncpassword at /home/<user>/.vnc/passwd with:
  vncpasswd
Change <user> to match your user (or change the path wherever you put the auth file)
Once the vnc server is started you can connect with a vnc client (like vinagre)
  vinagre 127.0.0.1:0
'''
from xpathwebdriver.default_settings import DefaultSettings

class Settings(DefaultSettings):
    # Check virtual_display_* options in https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/default_settings.py#L12
    # Most options will match those of pyvirtualdisplay.Display class, so check:
    # https://pyvirtualdisplay.readthedocs.io/en/latest/#usage
    virtual_display_enabled = True 
    virtual_display_backend = 'xvnc' # Force the backend
    # This are the kwargs passed to the pyvirtualdisplay backend class (XvfbDisplay, XvncDisplay or XephyrDisplay)
    virtual_display_backend_kwargs = dict(rfbauth='/home/<user>/.vnc/passwd')

