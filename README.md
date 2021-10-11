# xpathwebdriver

[![Codeship Status for joaduo/xpathwebdriver](https://app.codeship.com/projects/a77b1220-ecf1-0137-98b2-4e2936dc9ea3/status?branch=master)](https://app.codeship.com/projects/374749)

A python wrapper for interacting with Selenium through XPath and CSS selectors.
The main difference is that you can use use XPaths like:

```
//div/text()
```

Which will return you a string, something webdriver API makes more complicated.
Means you can write all your tests based on XPath without having to do heavy python manipulation
of the resulting objects.

Also adds:

- Interactive shell for testing XPath manually and easily against a live browser
- Multiple browser management
- Browser life management (wether to keep the browser open or kill it on exit)
  - Management is done through python contexts (`with` statement)
- Useful settings for local and remote (headless) testing
  - Also supports environment variables as settings
  - Plus allowing custom settings that you can also push through environment variables
- Screenshots comparison and diff management
- Virtual display management (so you can run "headless" in a remote instance)
  - you can use VNC to access the remote Browser

### Ubuntu quick installation

You can opt to use Chromium to simplify installation:

    sudo apt-get install -y python3-pip imagemagick findimagedupes tightvncserver xserver-xephyr xvfb unzip chromium-browser chromium-chromedriver
    sudo pip3 install xpathwebdriver Pillow ipython

You can quickly test it running:

    xpathshell

That will open an interactive shell with a browser object. Use TAB to autocomplete available API. Use `browser.driver` to directly access the webdriver object.

## General installation

```
pip install xpathwebdriver
```

1. Install xpathwebdriver using pip.
2. Install google chrome.
3. Download chromedriver for your chrome version and install it in your path.
   https://chromedriver.chromium.org/downloads
4. That generally should work on a modern Linux System (not tested but should also work on other oses).
   Try example in section below
5. For image comparison install `pip install Pillow`,  `findimagedupes` and `imagemagick` packages for your OS. (they are not automatically installed to keep basic requirments low)
   On ubuntu: `sudo apt install imagemagick findimagedupes`
6. For interactive shell install `pip install ipython`

Check "Installing Selenium" section for other browsers and details.

## Example

```python
from xpathwebdriver.browser import Browser

browser = Browser()
browser.get_url('https://duckduckgo.com/')
browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
# Using xpath that returns text
for idx, t in enumerate(browser.select_xpath('//div/text()')):
    print(idx, t)
# Using css selector which returns elements
for idx, elem in enumerate(browser.select_css('.result__title')):
    print(idx, elem.text)
```

## Documentation and tutorials

* Check `examples` directory
* The `BrowserAPI.md` file has a quick list of Browser's API
* Use `xpathsell -e` to print available environment variables for settings
* Use `xpathsell --settings-help` to print settings detailed documentation
  - or optionally check `xpathwebdriver/default_settings.py`

## IPython interactive shell

For a faster development and debugging cycles you can run an interactive shell which will let access the browser. First install ipython `pip install ipython` (not automatically installed to keep basic requirements low)

Then you can run the `xpathshell` in your terminal. You should see something like:

```
$ xpathshell
Python 3.7.5rc1 (default, Oct  8 2019, 16:47:45)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.9.0 -- An enhanced Interactive Python. Type '?' for help.

XpathBrowser in 'b' or 'browser' variables
 Current url: data:,
In [1]: b.get('github.com/joaduo/xpathwebdriver/')
INFO 05:53:35:  Current url: https://github.com/joaduo/xpathwebdriver/

```

Or pass the url in the command arguments. Eg: `xpathshell github.com/joaduo/xpathwebdriver/`

Inside IPython you can enter `browser.select_xpath?` to get documentation and can access API docs.

More `XpathBrowser` details at:

* https://github.com/joaduo/xpathwebdriver/blob/master/BrowserAPI.md
* https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/xpath_browser.py
* https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver_tests/test_XpathBrowser.py

### Using unittest library


```python
import unittest
from xpathwebdriver.webdriver_manager import get_browser

class SearchEnginesDemo(unittest.TestCase):
    def test_duckduckgo(self):
        with get_browser() as browser:
            browser.get_url('https://duckduckgo.com/')
            browser.fill('.//*[@id="search_form_input_homepage"]', 'xpathwebdriver\n')
```

Check a more options in the `examples` directory.

## Installing Selenium

To make sure you installed selenium and webdriver correctly use the code below:

```python
from selenium import webdriver
import time
driver = webdriver.Chrome() #or use another backend
driver.maximize_window()
driver.get('https://www.google.com')
print('You have 10 secs to check the browser window...')
time.sleep(10)
```

Find the easiest way to install selenium in your environment.

You can install driver for chrome and gecko from (OS like ubuntu do have .deb packages already)

* https://www.seleniumhq.org/download/#thirdPartyDrivers
* http://chromedriver.chromium.org/
* https://github.com/mozilla/geckodriver/releases
* PhantomJs: http://phantomjs.org/download.html (has the driver embedded)

Decompressed executables should be in yor PATH.
If you update python's `webdriver` package make sure you update browsers and drivers.

## Useful links for working with XPath

* https://addons.mozilla.org/es/firefox/addon/firebug/
* https://addons.mozilla.org/es/firefox/addon/firepath/
* http://ricostacruz.com/cheatsheets/xpath.html
* http://xpath.alephzarro.com/content/cheatsheet.html

## Killing processes hanging around

Depeding on your configuration from virtualdisplay and browser, processes like:

```
Xvnc
Xvfb
Xephyr
chromedriver
...
```

may keep hanging arround. You may want to kill them

```
# check the wanted process is alive
ps faux | grep Xvnc
# and you can kill it. If you are running as root, make sure you are not killing someone else's process too 
pkill Xvnc
```
