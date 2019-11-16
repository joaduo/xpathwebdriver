# xpathwebdriver

A python wrapper for interacting with Selenium through XPath and CSS selectors.
The main difference is that you can use use XPaths like:

```
//div/text()
```

Which will return you a string, something webdriver API makes more complicated.

## Quick install

```
pip install xpathwebdriver
```

1. Install xpathwebdriver using pip.
2. Install google chrome.
3. Download chromedriver for your chrome version and install it in your path.
   https://chromedriver.chromium.org/downloads
4. That generally should work on a modern Linux System (not tested but should also work on other oses).
   Try example below
5. For image comparison `pip install Pillow` and install `findimagedupes` and `imagemagick` packages for your OS

Check "Installing Selenium" section for other browsers and details.

## Example

```python
from xpathwebdriver.simple_xpath_browser import SimpleXpathBrowser

browser = SimpleXpathBrowser()
browser.get_url('https://duckduckgo.com/')
browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
# Using xpath that returns text
for idx, t in enumerate(browser.select_xpath('//div/text()')):
    print(idx, t)
# Using css selector which returns elements
for idx, elem in enumerate(browser.select_css('.result__title')):
    print(idx, elem.text)
```

## Running xpathshell

Install `pip install ipython`

Then you can run the `xpathshell` command:

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

Or directly from the command line

```
xpathshell duckduckgo.com
```

You can check `XpathBrowser` api at:

* https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver_tests/test_XpathBrowser.py
* https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/xpath_browser.py

### Using unittest library


```python
import unittest
from xpathwebdriver.simple_xpath_browser import SimpleXpathBrowser

class SearchEnginesDemo(unittest.TestCase):
    def setUp(self):
        # Get Xpath browser
        self.browser = SimpleXpathBrowser()

    def tearDown(self):
        # Make sure we quit those webdrivers created in this specific "level of life"
        del self.browser

    def test_duckduckgo(self):
        # Load a local page for the demo
        self.browser.get_url('https://duckduckgo.com/')
        # Type smoothtest and press enter
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
```

Check a more options in the `examples` directory.

## Installing Selenium

To make sure you installed selenium and webdriver correctly use the code below:

```python
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.google.com')
print('You can 10 secs to check the browser window')
time.sleep(10)
```

Find the easiest way to install selenium in your environment.

Then install driver for chrome and gecko from:

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
