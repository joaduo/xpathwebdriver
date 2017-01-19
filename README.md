# Xpathwebdriver

Python wrapper for interacting with Selenium through XPath paths.

## Example

Nicer tests for web sites.

```python
import unittest
from xpathwebdriver.simple_xpath_browser import SimpleXpathBrowser

class SearchEnginesDemo(unittest.TestCase):
    def setUp(self):
        # Get Xpath browser
        self.browser = SimpleXpathBrowser()

    def tearDown(self):
        # Make sure we quit those webdrivers created in this specific level of life
        del self.browser

    def test_duckduckgo(self):
        # Load a local page for the demo
        self.browser.get_url('https://duckduckgo.com/')
        # Type smoothtest and press enter
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'xpathwebdriver\n')
```

## Install
```
pip install xpathwebdriver
```
The selenium package requires you to download drivers

* Firefox: https://github.com/mozilla/geckodriver/releases
* Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
* PhantomJs: http://phantomjs.org/download.html

Decompressed executables should be in yor PATH.

## Running the interactive shell

Once installed run in command line:
```
xpathshell
```
Or:
```
xpathshell github.com/joaduo/xpathwebdriver
```
To open https://github.com/joaduo/xpathwebdriver

You will get an IPython interactive shell like:
```
XpathBrowser in 'b' or 'browser' variables
 Current url: https://github.com/joaduo/xpathwebdriver
In [1]:
```

## Useful links for working with XPath

* https://addons.mozilla.org/es/firefox/addon/firebug/
* https://addons.mozilla.org/es/firefox/addon/firepath/
* http://ricostacruz.com/cheatsheets/xpath.html
* http://xpath.alephzarro.com/content/cheatsheet.html
