# Xpathwebdriver
Simpler webdriver API through a wrapper

## Better API for accessing Selenium

Nicer tests for web sites.

```python
import unittest
from xpath_webdriver.simple_xpath_browser import SimpleXpathBrowser

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
        self.browser.fill(".//*[@id='search_form_input_homepage']", 'smoothtest\n')
```

## Install
```
pip install xpathwebdriver
```

## Running the interactive shell

Once installed run `xpathshell` in command line or:

```
xpathshell github.com/joaduo/xpathwebdriver
```

To open https://github.com/joaduo/xpathwebdriver
