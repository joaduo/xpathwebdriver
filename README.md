# Xpathwebdriver

Python wrapper for interacting with Selenium through XPath and CSS selectors.
The main difference is that you can use use XPaths like:
```
//div/text()
```
Which will return you a string, somethin selenium does not support easily.
E.g. you could do:
```
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

## Example

Unit Test for web site.

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

## Install
Make sure you installed selenium and webdriver (and that they are working)
You can test selenium with:
```
```
Then you can install this wrapper easily.

```
pip install xpathwebdriver
```
The selenium package requires you to download drivers

* Firefox: https://duckduckgo.com/mozilla/geckodriver/releases
* Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
* PhantomJs: http://phantomjs.org/download.html (has the driver embedded)

Decompressed executables should be in yor PATH.

If you update python's `webdriver` package make sure you update browsers and drivers.

## Running the interactive shell

Install ipython package (in ubuntu probably you can install python-ipython package)
```
pip install ipython
```
You then can run from command line
```
xpathshell
```
Or opening a website:
```
xpathshell duckduckgo.com
```
To open https://duckduckgo.com

You will get an IPython interactive shell like:
```
XpathBrowser in 'b' or 'browser' variables
 Current url: https://duckduckgo.com/
In [1]:
```

## Useful links for working with XPath

* https://addons.mozilla.org/es/firefox/addon/firebug/
* https://addons.mozilla.org/es/firefox/addon/firepath/
* http://ricostacruz.com/cheatsheets/xpath.html
* http://xpath.alephzarro.com/content/cheatsheet.html
