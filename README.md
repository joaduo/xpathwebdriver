# Xpathwebdriver

Python wrapper for interacting with Selenium through XPath and CSS selectors.
The main difference is that you can use use XPaths like:

```
//div/text()
```

Which will return you a string, something selenium does not support easily.
E.g. you could do:

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

### Installing selenium and the browser driver
Make sure you installed selenium and webdriver and that they are working.
You can test selenium with:

```python
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.google.com')
print('You can 10 secs to check the browser window')
time.sleep(10)
```
Find the easiest way to install selenium in your environment, for example
in ubuntu, you can do:

```
apt install python-pip python-selenium
# Or in case of python3 use: python3-pip python3-selenium packages
```
Then install driver for chrome and gecko from:

* https://www.seleniumhq.org/download/#thirdPartyDrivers
* http://chromedriver.chromium.org/
* https://github.com/mozilla/geckodriver/releases
* PhantomJs: http://phantomjs.org/download.html (has the driver embedded)

Decompressed executables should be in yor PATH.
If you update python's `webdriver` package make sure you update browsers and drivers.

### Installing Xpathwebdriver

Once selenium is working you can easily install this wrapper.

```
pip install xpathwebdriver
```

## Running the interactive shell

Install ipython package (in Ubuntu probably you can install ipython or ipython3 package)

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

You can check `XpathBrowser` api at:

* https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver_tests/test_XpathBrowser.py
* https://github.com/joaduo/xpathwebdriver/blob/master/xpathwebdriver/xpath_browser.py

## Useful links for working with XPath

* https://addons.mozilla.org/es/firefox/addon/firebug/
* https://addons.mozilla.org/es/firefox/addon/firepath/
* http://ricostacruz.com/cheatsheets/xpath.html
* http://xpath.alephzarro.com/content/cheatsheet.html
