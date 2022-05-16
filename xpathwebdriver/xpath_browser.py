# -*- coding: utf-8 -*-
'''
xpathwebdriver
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
import sys
import time
import os
from functools import wraps
from contextlib import contextmanager
from urllib.parse import urlparse, urlunparse, urljoin, parse_qsl, unquote_plus

import parsel
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException,\
    TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .logger import Logger
from .validators import is_valid_netloc


class Url:
    '''A url object that can be compared with other url orbjects
    without regard to the vagaries of encoding, escaping, and ordering
    of parameters in query strings.
    from http://stackoverflow.com/questions/5371992/comparing-two-urls-in-python
    '''
    def __init__(self, url):
        if not isinstance(url, Url):
            self._orig = parts = urlparse(url)
            _query = frozenset(parse_qsl(parts.query))
            _path = unquote_plus(parts.path).rstrip('/')
            parts = parts._replace(query=_query, path=_path)
            self.parts = parts
        else:
            self._orig = url._orig
            self.parts = url.parts

    def replace(self, **kwargs):
        return Url(urlunparse(self._orig._replace(**kwargs)))

    def get_original(self):
        '''
        Get original url.
        '''
        return urlunparse(self._orig)

    def get_path_and_on(self):
        '''
        Get (path + params + query + fragment) as string from original url.
        '''
        return str(self.replace(scheme='', netloc=''))

    def get_scheme_netloc(self):
        return str(self.replace(path='', params='', query='', fragment=''))

    def get_scheme_netloc_path(self):
        return str(self.replace(params='', query='', fragment=''))

    def cmp_path(self, url):
        url = self._convert(url)
        return self.get_path_and_on() == url.get_path_and_on()

    @staticmethod
    def are_equal(url_a, url_b):
        return Url(url_a) == Url(url_b)

    def __eq__(self, other):
        other = self._convert(other)
        return self.parts == other.parts

    def _convert(self, url):
        if isinstance(url, str):
            url = Url(url)
        return url

    def __hash__(self):
        return hash(self.parts)

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.get_original())

    def __str__(self):
        return self.get_original()


def implicit_xpath_wait(method):
    @wraps(method)
    def wrapper(self, xpath, *a, **kw):
        max_wait = wrapper._implicit_max_wait or self._implicit_max_wait
        condition = wrapper._implicit_wait_condition or self._implicit_wait_condition
        if max_wait:
            self.wait_condition(condition(xpath), max_wait)
        return method(self, xpath, *a, **kw)
    wrapper._implicit_max_wait = None
    wrapper._implicit_wait_condition = None
    return wrapper


class XpathBrowser:
    '''
    Class for making Webdriver more xpath-friendly.
    This class is designed to be framework independent, to be reused by other
    testing frameworks.
    '''
    Url = Url

    def __init__(self, webdriver, base_url=None, logger=None, settings=None):
        '''
        :param base_url: common base url (e.g: http://example.com, http://example.com/some/common/path) 
            Used to build URL for all methods accepting the "path" argument. 
        :param webdriver: selenium's webdriver object (connected to Firefox, Chrome, etc...)
        :param logger: You can optionally pass a xpathwebdriver.Logger instance (or a child class's instance)  
        :param settings: xpathwebdriver settings object.
        '''
        settings = settings or {}
        self.settings = settings
        self.log = logger or settings.get('logger', Logger(self.__class__.__name__))
        assert webdriver, 'You must provide a webdriver'
        self._driver = webdriver
        # Initialize values
        self._base_url = base_url
        self._sleep_multiplier = self.settings.get('xpathbrowser_sleep_multiplier', 1)
        self._sleep_time = self.settings.get('xpathbrowser_sleep_default_time', 1)
        self._max_wait = self.settings.get('xpathbrowser_max_wait', 5)
        self._implicit_max_wait = self.settings.get('xpathbrowser_implicit_max_wait', 0)

    def _implicit_wait_condition(self, xpath):
        def condition(browser):
            return browser._select_xpath(xpath, single=False, wait=False)
        return condition

    @property
    def driver(self):
        return self.get_driver()

    @property
    def base_url(self):
        return self._base_url

    def set_base_url(self, base_url):
        '''
        Set base URL. (in order to build full URLs passing the path eg: browser.get_page('/path/page.html'))

        :param base_url: base URL string eg:"http://example.com/". 
            You can even  add more details after the host like:"http://example.com/common_path/" 
        '''
        self._base_url = self.clean_url(base_url)

    def get_driver(self):
        '''
        Return selenium's webdriver instance
        Or you can directly access it via browser.driver attribute
        '''
        assert self._driver, 'driver was not initialized'
        return self._driver

    @property
    def current_path(self):
        '''
        Get (path + params + query + fragment) as string from current url.
        '''
        return self.Url(self.current_url).get_path_and_on()

    @property
    def current_url(self):
        '''
        Return the current page's URL. (from webdriver instance) 
        '''
        return self.driver.current_url

    def build_url(self, path):
        '''
        Build a full URL from a URL path (path and on)
        
        :param path: path and on eg:"/blog/123?param=1"
        '''
        base_url = self._base_url or self.Url(self.current_url).get_scheme_netloc_path()
        assert base_url, 'No base_url set for building urls'
        if path.startswith('/') and self.settings.get('xpathbrowser_paths_like_html', True):
            #building url relative to the server's root
            base_url = self.Url(base_url).get_scheme_netloc()
        return urljoin(base_url, path)

    def get(self, url, condition=None):
        '''
        Smarter way to open an url. It cleans url. You can pass what you would use in a browser.
        :param url: url string (eg: github.com)
        :param condition: optional condition script or functor passed to the `wait_condition` method
        '''
        self.get_url(self.clean_url(url), condition)

    def clean_url(self, url):
        orig = url
        if Url(url).parts.netloc:
            return url
        if not url.startswith('//'):
            # Add '//' so urlparse detects domain
            url = '//' + url
        url = Url(url)
        if not url.parts.netloc or not is_valid_netloc(url.parts.netloc):
            msg = ('No domain or invalid domain in %r. '
                   'Provide scheme to avoid this check', orig)
            self.log.e(msg)
            raise ValueError(msg)
        if not url.parts.scheme:
            url = url.replace(scheme=self.settings.get('xpathbrowser_default_scheme', 'http'))
        return str(url)

    def get_url(self, url, condition=None):
        '''
        Open a page in the browser controlled by webdriver.
        
        :param path: full URL of the page
        :param condition: optional condition script or functor passed to the `wait_condition` method
        '''
        driver = self.driver
        if (url.startswith('https')
            and hasattr(webdriver, 'PhantomJS')
            and isinstance(driver, webdriver.PhantomJS)):
            self.log.d('PhantomJS may fail with https if you don\'t pass '
                       'service_args=[\'--ignore-ssl-errors=true\']'
                       ' Trying to fetch {url!r}'.format(url=url))
        self.log.d('Fetching page at {url!r}'.format(url=url))
        driver.get(url)
        # Errors
        msg = 'Couldn\'t load page at {url!r}'.format(url=url)
        if condition and not self.wait_condition(condition):
            raise LookupError(msg)
        if self.current_url == u'about:blank':
            raise LookupError(msg + '. Url is u"about:blank"')
        if not self.Url.are_equal(url, self.current_url):
            self.log.d('For {url!r} we got {current!r}.'
                       .format(url=url, current=self.current_url))

    def get_page(self, path, condition=None):
        '''
        Open a page in the browser controlled by webdriver.
        
        :param path: path and on eg:"/blog/123?param=1" to get the page from
        :param condition: optional condition script or functor passed to the `wait_condition` method
        '''
        self.get_url(self.build_url(path), condition)

    def get_page_once(self, path, condition=None):
        '''
        Open a page only once in the browser controlled by webdriver.
        If the page is already opened, then no reloading is performed.
        Beware: if a page implies redirection, it will be reloaded anyway.
        (becaus URL changes and it does not match the value of `path`)
        
        :param path: path and on eg:"/blog/123?param=1" to get the page from
        :param condition: optional condition script or functor passed to the `wait_condition` method
        '''
        # Remove user credentials (they are not shown in browser)
        url = self.build_url(path)
        parts = urlparse(self.build_url(path))
        if '@' in parts.netloc:
            netloc = parts.netloc.split('@')[1]
            url = urlunparse(parts._replace(netloc=netloc))
        # Check if page was already loaded
        if not self.Url.are_equal(url, self.current_url):
            # Url is different, load new page
            self.get_page(path, condition)
        else:
            # Page already loaded
            self.log.d('Page already loaded once: %r' % url)

    _default_condition = 'return "complete" == document.readyState;'

    def wait_condition(self, condition=None, max_wait=None):
        '''
        Active wait (polling) function, for a specific condition inside a page.
        
        Condition may be:
          - a functor: a function receiving this xbrowser object as argument
            returns True if condition was met, eg:

            def condition(xbrowser):
               # We want to know if the email was loaded
               return xbrowser.select_xsingle('//a[@id="EmailSubject"]') == u'Welcome to our service'

          - a string javascript function, eg:
            """
            return "complete" == document.readyState;
            """

            The javascript must have the return statement at the end,
            which must be True if the condition is met
            
        If you don't supply any condition, then this default javascript condition
        will be used:
            return "complete" == document.readyState;

        Sometimes that condition is not good enough, so you may use a python
        function or a javascript condition to be sure you got the page/result
        loaded.

        :param condition: functor or javascript string of condition checking logic.
        :param max_wait: Max amount of time to wait for condition to be true (per try round).
                         First try is 1/10th of this value, second 2/10th and so on...
        :param print_msg: print debug message (debugging purpose)
        '''
        condition = condition if condition else self._default_condition
        if isinstance(condition, str):
            # Its a javascript script
            def condition_func(xbrowser):
                return xbrowser.get_driver().execute_script(condition)
            condtn = condition_func
        else:
            condtn = condition
        # first start waiting a tenth of the max time
        # then increase time adding a tenth until getting the 100% of wait time
        parts = 10
        max_wait = max_wait or self._max_wait
        assert 0 < max_wait , 'max_wait must be greater than zero'
        delta = float(max_wait) / float(parts)
        for try_num in range(1, parts + 1):
            loaded = condtn(self)
            if loaded:
                self.log.d('Condition "%s" is True.' % condition)
                break
            if try_num < parts:
                self.log.d('Waiting condition "%s" to be True.' % condition)
                time.sleep(delta * try_num)
        # If condition was not satisfied print debug message
        if not loaded:
            self.log.d('Page took too long to load. Increase max_wait parameter'
                   ' or modify object\'s "_max_wait" attribute.')
        # Return whether condition was satisfied
        return loaded

    def _get_xpath_script(self, xpath, single=True):
        '''
        Get Javascript code for getting single or multiple nodes from webdriver
        page's DOM.
        Returns web element, attribute or text depending o the xpath specified.

        :param xpath: xpath to build the script from
        :param single: select only a single node
        '''
        script_single = '''
var xpath = %(xpath)r;
//XPathResult.FIRST_ORDERED_NODE_TYPE = 9
var FIRST_ORDERED_NODE_TYPE = 9;
var element = document.evaluate(xpath, document, null, FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
return extract_element(element);
            '''
        script_multiple = '''
var xpath = %(xpath)r;
//XPathResult.ORDERED_NODE_ITERATOR_TYPE = 5
var ORDERED_NODE_ITERATOR_TYPE = 5;
var es = document.evaluate(xpath, document, null, ORDERED_NODE_ITERATOR_TYPE, null);
var r = es.iterateNext();
var eslist = [];
while(r){
    eslist.push(extract_element(r));
    r = es.iterateNext();
}
return eslist;
        '''
        script = script_single if single else script_multiple
        return self._get_extract_element() + script % locals()

    def _get_css_selector_script(self, selector, single=True):
        '''
        Get Javascript code for getting single or multiple nodes from webdriver
        page's DOM.
        Returns web element, attribute or text depending o the selector specified.

        :param selector: selector to build the script from
        :param single: select only a single node
        '''
        script_single = '''
var selector = %(selector)r;
var element = document.querySelector(selector);
return extract_element(element);
            '''
        script_multiple = '''
var selector = %(selector)r;
var es = document.querySelectorAll(selector);
var eslist = [];
for(var idx=0; idx < es.length; idx++){
    eslist.push(extract_element(es[idx]));
}
return eslist;
        '''
        script = script_single if single else script_multiple
        return self._get_extract_element() + script % locals()

    def _get_extract_element(self):
        extract_element = '''
function extract_element(elem){
    if(!elem){
        return elem;
    }
    var elem = elem;
    //elem.noteType == 1 //web element
    if(elem.nodeType == 2){
      //attribute
      elem = elem.value;
    }
    if(elem.nodeType == 3){
      //text()
      elem = elem.wholeText;
    }
    return elem;
}
        '''
        return extract_element

    def xpath(self, xpath, single=False, wait=False):
        '''
        Select HTML nodes given an xpath.
        May return:
            - webdriver's web element
            - strings (if xpath specifies @attribute or text())

        :param xpath: xpath's string eg:"/div[@id='example']/text()"
        :param single: if True, returns only the first node
        :param wait: explicit wait using self._implicit_wait_condition method
        :returns: list of selected Webelements or strings
        '''
        return self._select_xpath(xpath, single=single, wait=wait)

    def select_xpath(self, xpath, wait=False):
        '''
        Select HTML nodes given an xpath.
        May return:
            - webdriver's web element
            - strings (if xpath specifies @attribute or text()) 

        :param xpath: xpath's string eg:"/div[@id='example']/text()"
        :param wait: explicit wait using self._implicit_wait_condition method
        :returns: list of selected Webelements or strings
        '''
        return self._select_xpath(xpath, single=False, wait=wait)

    @implicit_xpath_wait
    def select_xsingle(self, xpath, wait=False):
        '''
        Select first node specified by xpath.
        If xpath is empty, it will raise an exception
        Implicitly wait for the xpath to appear (must have first item at list)

        :param xpath: xpath's string eg:"/div[@id='example']/text()"
        :param wait: explicit wait using self._implicit_wait_condition method
        :returns: Webelement or string (depeding on the passed xpath)
        '''
        result = self._select_xpath(xpath, single=True, wait=wait)
        if result is None:
            raise LookupError(f'Could not find first element of xpath={xpath}')
        return result

    def _select_xpath(self, xpath, single, wait):
        '''
        Select nodes specified by xpath

        :param xpath: xpath's string eg:"/div[@id='example']/text()"
        :param single: if True, returns only the first node
        :param wait: explicit wait using self._implicit_wait_condition method
        '''
        # Explicit wait flag
        if wait and self._implicit_max_wait:
            self.wait_condition(self._implicit_wait_condition(xpath), self._implicit_max_wait)
        return self._select(xpath, single, select_type='xpath')

    def _select(self, select_expr, single, select_type, with_selector=True):
        '''
        Select nodes specified by xpath

        :param select_expr: xpath or css selector
        :param single: if True, returns only the first node
        :param select_type: type of select_expr passed, ie: 'xpath' or 'css'
        :param with_selector: Wrapp elements with Xpath selector from parsel library
        '''
        dr = self.driver
        try:
            if select_type == 'xpath':
                script = self._get_xpath_script(select_expr, single)
            else:
                script = self._get_css_selector_script(select_expr, single)
            result = dr.execute_script(script)
        except WebDriverException as e:
            msg = (
                'WebDriverException: Could not select {select_type} {select_expr!r} '
                'for page {dr.current_url!r}\n Error:\n {e}'.format(
                    **locals()))
            raise LookupError(msg)
        if with_selector:
            if single:
                result = self._add_selector(result)
            else:
                result = [self._add_selector(e) for e in result]
        return result

    def css(self, selectors):
        return self._select(selectors, single=False, select_type='css')

    def select_css(self, selectors):
        return self._select(selectors, single=False, select_type='css')

    def select_css_single(self, selectors):
        return self._select(selectors, single=True, select_type='css')

    def fill(self, xpath, value, clear=True, javascript_safe=False):
        '''
        Fill input field on page:
          - selects Webelement
          - sends keystroke to it

        :param xpath: xpath's string eg:"./input[@id='example']"
        :param value: string to fill the input with
        :param clear: if True clear input before writing
        :param javascript_safe: if True avoid javascript problem (assigning value to field)
        '''
        element = self.select_xsingle(xpath)
        if clear:
            element.clear()
        if javascript_safe:
            self.execute_script("arguments[0].value = arguments[1]", element, value)
        else:
            element.send_keys(value)

    def click(self, xpath):
        '''
        Click element in xpath:
          - selects Webelement
          - sends click to it

        :param xpath: xpath's string eg:"./button[@id='send_form']"
        '''
        element = self.select_xsingle(xpath)
        try:
            element.click()
        except WebDriverException as e:
            msg = (
                '\nWebDriverException: Could not click {xpath!r}'
                'for page {self.current_url!r}\n Error:\n {e}'.format(
                    **locals()))
            e.msg += msg
            raise e

    SLEEP_SHRINK='<'
    SLEEP_GROW='>'
    SLEEP_GROW_OR_SHRINK='><'
    SLEEP_FROZEN='='
    def sleep(self, timeout=None, condition=SLEEP_GROW):
        '''
        Useful sleep method (workaround for many webdriver's problem)
        :param timeout: if specified, amount of seconds to wait, else use settings default value.
        :param condition: when to multiply time by `self._sleep_multiplier`
                        can be a string like '>','<', '><', '='
                        SLEEP_GROW:           multiply when mutiplier > 1 (grows time)
                        SLEEP_SHRINK:         multiply when multiplier < 1 (shrinks time)
                        SLEEP_GROW_OR_SHRINK: multiply always
                        SLEEP_FROZEN:         never multiply/scale
        '''
        seconds = (timeout or self._sleep_time)
        mult = self._sleep_multiplier
        if ((mult > 1 and '>' in condition)
        or  (mult < 1 and '<' in condition)):
            seconds *= mult
        time.sleep(seconds)

    def wipe_alerts(self, timeout=0.5):
        '''
        Wipe browser's alert dialogs. Useful for unblocking webdriver.

        :param timeout: max wait for alert in second (default=0.5)
        '''
        try:
            WebDriverWait(self.driver, timeout
                          ).until(expected_conditions.alert_is_present(),
                                  'Timed out waiting alert.')
            alert = self.driver.switch_to_alert()
            alert.accept()
        except TimeoutException:
            pass

    _quick_sshot_count = 0

    def quick_screenshot(self, to_path=None):
        '''
        Take a quick screenshot saving the file to the current dir.
        It will autonumerate screenshots. 001.quick_screenshot.png ...etc
        '''
        self._quick_sshot_count += 1
        filename = '%03d.quick_screenshot.png' % self._quick_sshot_count
        if to_path:
            path = os.path.join(to_path, filename)
        else:
            path = filename
        self.log.i('Saving screenshot to: %r' % filename)
        self.save_screenshot(path)

    def save_screenshot(self, path, width=None, height=None, windowHandle='current'):
        '''
        Take a screenshot and save it to the path specified in filename
        :param path: path to save the screenshot file to
        :param width: optional. set window size width
        :param height: optional. set window size height
        :param windowHandle: optional. if more than one window, they you may need to set window handler
        '''
        previous = None
        try:
            if width or height:
                previous = self.driver.get_window_size(windowHandle)
                width = width or previous['width']
                height = height or previous['height']
                self.driver.set_window_size(width, height, windowHandle)
            self.driver.save_screenshot(path)
        finally:
            if previous:
                self.driver.set_window_size(previous['width'],
                            previous['height'], windowHandle=windowHandle)

    def execute_script(self, script, *args):
        '''
        Execute javascript in the Browser.
        Will return a value if the specified script returns a value.
        :param script: javascript script to be executed. 
        '''
        return self.driver.execute_script(script, *args)

    def fill_form(self, clear=True, javascript_safe=True, **inputs):
        '''
        Fill a form given a {<input/textarea name>:<value>} dictionary
        Example:
            browser.fill_form(name='John', surname='Doe', email='john.doe@gmail.com')
        Is equivalent to doing:
            browser.fill_form_xpath({'//input[@name="name"] | //textarea[@name="name"]':'John', ...})
        :param clear: if True clear input before writing
        :param javascript_safe: if True avoid javascript problem (assigning value to field)
        :param inputs: kwargs dictionary of <form's field name>=<value>
        '''
        self.fill_form_attr('name', inputs, clear, javascript_safe)

    def fill_form_attr(self, attr, inputs, clear=True, javascript_safe=False):
        '''
        :param attr: html tag attribute to build the xpath with
        :param inputs: dictionary {<form's field attr value>:<value to enter>}
        :param clear: if True clear input before writing
        :param javascript_safe: if True avoid javascript problem (assigning value to field)
        '''
        xpath = '//input[@{0}={1!r}] | //textarea[@{0}={1!r}]'
        inputs = {xpath.format(attr,name):value
                  for name, value in inputs.items()}
        self.fill_form_xpath(inputs, clear, javascript_safe)

    def fill_form_xpath(self, inputs, clear=True, javascript_safe=False):
        '''
        :param inputs: dictionary of {<form's field xpath>:<value to enter>}
        :param clear: if True clear input before writing
        :param javascript_safe: if True avoid javascript problem (assigning value to field)
        '''
        for xpath, value in inputs.items():
            self.fill(xpath, value, clear, javascript_safe)

    def fill_form_ordered(self, items, attr='name', clear=True, javascript_safe=False):
        '''
        Fill a form given a [(<input/textarea name>,<value>),...] list
        :param items: list of [(name, value), ...]
        :param attr: html tag attribute to build the xpath. default='name'
        :param clear: if True clear input before writing
        :param javascript_safe: if True avoid javascript problem (assigning value to field)
        '''
        for name, value in items:
            self.fill('//input[@{0}={1!r}] | //textarea[@{0}={1!r}]'
                      .format(attr, name), value, clear, javascript_safe)

    def get_remote_credentials(self):
        drv = self.driver
        return dict(command_executor=drv.command_executor._url,
                    session_id=drv.session_id)

    @contextmanager
    def iframe(self, xpath, max_wait=None):
        try:
            iframe = self.select_xsingle(xpath)
            self.driver.switch_to.frame(iframe)
            yield iframe
        finally:
            self.driver.switch_to.default_content()

    @contextmanager
    def window(self, index=1, timeout=5, switch_back_to=-1, close=True):
        """
        :param index: index of the handle in driver.window_handles of the expected window
        :param timeout: How much to wait for the new window (0 or None for no timeout)
        :param switch_back_to: Switch back to this handle.
            - you can pass the handle id
            - or absolute index of the handle in driver.window_handles
        :param close: close the expected window
        """
        try:
            waiting = step = (timeout or 2) / 10
            while len(self.driver.window_handles) <= index and (not timeout or waiting < timeout):
                self.sleep(waiting)
                waiting += step
            if len(self.driver.window_handles) <= index:
                raise LookupError(f'Could not finde windows at index={index}')
            win = self.driver.window_handles[index]
            self.driver.switch_to.window(win)
            yield win
        finally:
            if close:
                self.driver.close()
            if switch_back_to:
                if isinstance(switch_back_to, int):
                    switch_back_to = self.driver.window_handles[index + switch_back_to]
                self.driver.switch_to.window(switch_back_to)

    def _add_selector(self, element):
        if isinstance(element, WebElement):
            w = WebElementSelector(element)
            element.xpath = w.xpath
            element.css = w.css
            element.selector = w.selector
        return element

    def get_selector(self, element):
        return WebElementSelector(element).selector()

    def wait_xpath(self, xpath, condition=None, max_wait=None):
        condition = condition or self._implicit_wait_condition(xpath)
        return self.wait_condition(condition, max_wait)


class WebElementSelector:
    def __init__(self, element):
        self.__wrapped__ = element

    def selector(self):
        html = self.__wrapped__.get_attribute('outerHTML')
        sel = parsel.Selector(html)
        return sel

    def xpath(self, xpath, namespaces=None, **kwargs):
        return self.selector().xpath(xpath, namespaces, **kwargs)

    def css(self, query):
        return self.selector().css(query)

