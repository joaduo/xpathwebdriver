'''
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()

from selenium import webdriver
from pyvirtualdisplay import Display
from threading import RLock
from functools import wraps
from selenium.common.exceptions import UnexpectedAlertPresentException, WebDriverException
from .base import XpathWdBase, singleton_decorator
from xpathwebdriver.levels import TEST_ROUND_LIFE, MANAGER_LIFE
from selenium.webdriver.remote.webdriver import WebDriver
import os
import logging
import json
from collections import namedtuple
import shlex

logger = logging.getLogger(__name__)


def synchronized(lock):
    '''
    Thread synchronization decorator. (for several methods with same lock, use
    re-entrant lock)
    :param lock: lock object (from threading package for example)
    '''
    def wrap_method(method):
        @wraps(method)
        def newFunction(*args, **kw):
            with lock:
                return method(*args, **kw)
        return newFunction
    return wrap_method


WdriverCfg = namedtuple('WdriverCfg', 'browser context shared level')


@singleton_decorator
class WebdriverManager(XpathWdBase):
    '''
    This is a Global Manager for the Webdriver's instances available.
    '''
    # Thread lock for methods in this class
    _methods_lock = RLock()

    def __init__(self):
        # Set of locked webdrivers
        self._locked = set()
        # Set of released webdrivers
        self._released = set()
        # Pool of drivers {wdriver:WdriverCfg}
        self._wdriver_pool = {}
        # Virtual display object where we start webdrivers
        self._virtual_display = None
        # Any browser without specified level
        self._current_context_level = 0
        # Marks those contexts already taken
        self._context_name_level = {}

    @synchronized(_methods_lock)
    def enter_level(self, level=None, base_url=None, name='', browser_name=None):
        '''
        :param level: webdriver's level of life we are entering
        :param base_url: optional set a base url for the browser (to specify paths)
        :param name: optional level's name (mainly for logging purposes)
        :param browser_name: optional browser name string (eg: 'Firefox', 'Chrome', 'PhantomJs')
        '''
        self.log.w('DEPRECATED method enter_level, use enter get_browser')
        # override level
        self._current_context_level += 1
        level = self._current_context_level
        self.init_level(level, browser_name, context_name=name)
        return BrowserContextManager(self, level, base_url, name, browser_name)

    @synchronized(_methods_lock)
    def get_browser(self, context_name='default', browser=None):
        '''
        :param name: optional context's name (mainly for logging purposes)
        :param browser: optional browser name string (eg: 'Firefox', 'Chrome', 'PhantomJs')
        '''
        self._current_context_level += 1
        level = self._current_context_level
        self.init_level(level, browser, context_name)
        return BrowserContextManager(self, level, context_name=context_name, browser_name=browser)

    @synchronized(_methods_lock)
    def exit_level(self, level):
        '''
        :param level: webdriver's level of life we are exiting
        '''
        def quit_wdriver(wdriver, container):
            cfg = self._wdriver_pool[wdriver]
            if self._quit_failed_webdriver(wdriver):
                self.log.d('Quitting failed webdriver %s', wdriver)
                container.remove(wdriver)
                self._wdriver_pool.pop(wdriver)
            # Quit if exiting the level (but keep if shared browser, started by some other process)
            elif (cfg.level >= level 
            and not cfg.shared
            and not self.global_settings.get('webdriver_browser_keep_open')):
                self.log.d('Quitting exited level webdriver %s', wdriver)
                container.remove(wdriver)
                self._quit_webdriver(wdriver)
                self._wdriver_pool.pop(wdriver)
            else:
                self.log.d('Keeping webdriver %s', wdriver)
        # Make copies of sets, we are going to modify them
        for wdriver in self._released.copy():
            quit_wdriver(wdriver, self._released)
        for wdriver in self._locked.copy():
            quit_wdriver(wdriver, self._locked)

    @synchronized(_methods_lock)
    def init_level(self, level, browser_name, context_name):
        '''
        Initialize webdriver for a specific Life Level.
        There are two possibilities:
          1- no webdriver was initialized on previous level => init it 
          2- there is a webdriver for the browser selected, no action is performed.
        :param level: webdriver's level of life we are entering
        '''
        # Get rid of non-responding browsers
        self.quit_all_failed_webdrivers()
        # Get the set of released webdrivers for the selected browser
        released = self.get_available_set(browser_name, context_name)
        # If no webdriver available, then create a new one 
        if not released:
            # Create webdriver if needed
            browser_name = self.get_browser_name(browser_name)
            wdriver, shared = self._new_webdriver(browser_name, level, context_name)
            self._wdriver_pool[wdriver] = WdriverCfg(browser_name, context_name, shared, level)
            self._released.add(wdriver)

    @synchronized(_methods_lock)
    def get_available_set(self, browser_name, context_name):
        '''
        Return the set of avialable webdrivers for the current Browser selected
        (in global configuration)
        '''
        browser = self.get_browser_name(browser_name)
        browser_set = set([wdriver
                           for wdriver,cfg in self._wdriver_pool.items()
                           if cfg.browser == browser and cfg.context == context_name])
        return (self._released & browser_set)

    def _new_webdriver(self, browser, level, context_name, args=None, kwargs=None):
        args = args or []
        kwargs = kwargs or self.global_settings.get('webdriver_browser_kwargs', {})
        browser = self.expand_browser_name(browser)
        # Setup display before creating the browser
        self.start_display()
        credentials = self._load_credentials()
        shared = False
        if (context_name not in self._context_name_level
        and context_name in credentials):
            driver = self._build_remote(**credentials[context_name])
            if driver:
                shared = True
                self._context_name_level[context_name] = level
        if not shared:
            if browser == 'PhantomJS':
                self._append_service_arg('--ignore-ssl-errors=true', kwargs)
            if (browser == 'Firefox'
            and self.global_settings.get('webdriver_browser_profile',
                self.global_settings.get('webdriver_firefox_profile'))
            and not args and 'firefox_profile' not in kwargs):
                # Update with profile specified from config
                fp = webdriver.FirefoxProfile(self.global_settings.get('webdriver_browser_profile',
                                              self.global_settings.get('webdriver_firefox_profile')))
                kwargs['firefox_profile'] = fp
            if (browser == 'Chrome'
            and self.global_settings.get('webdriver_browser_profile')
            and not args and 'chrome_options' not in kwargs):
                from selenium.webdriver.chrome.options import Options
                chrome_options = Options()
                if os.name == 'posix' and os.geteuid() == 0:
                    self.log.w('Passing --no-sandbox flag to Chrome (running as root)')
                    chrome_options.add_argument('--no-sandbox')
                if self.global_settings.get('webdriver_browser_profile'):
                    profile_dir = self.global_settings.get('webdriver_browser_profile')
                    profile_dir = os.path.abspath(profile_dir)
                    profile_dir = shlex.quote(profile_dir)
                    chrome_options.add_argument(f'--user-data-dir={profile_dir}')
                #self.log.w('Adding --disable-application-cache')
                #chrome_options.add_argument('--disable-application-cache')
                #chrome_options.add_argument('--incognito')
                kwargs['chrome_options'] = chrome_options
            driver = getattr(webdriver, browser)(*args, **kwargs)
        if self.global_settings.get('webdriver_window_size'):
            h,w = self.global_settings.get('webdriver_window_size')
            driver.set_window_size(h,w)
        return driver, shared

    def _load_credentials(self):
        path = self.global_settings.get('webdriver_remote_credentials_path')
        if not path:
            return {}
        with open(path) as fp:
            return json.load(fp)

    def _build_remote(self, command_executor, session_id):
        original_execute = WebDriver.execute
        non_local = dict(first_run=True)
        def _patched_execute(self, command, params=None):
            if command == "newSession" and non_local['first_run']:
                non_local['first_run'] = False
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return original_execute(self, command, params)
        # Patch the function before creating the driver object
        WebDriver.execute = _patched_execute
        driver = webdriver.Remote(command_executor=command_executor)
        driver.session_id = session_id
        # Replace the patched function with original function
        WebDriver.execute = original_execute
        try:
            driver.get_window_size()
        except WebDriverException as e:
            logger.warning(f'Exception {e} while trying to connect to a remote shared webdriver.'
                           ' Creating new local browser...')
            driver = None
        return driver

    def _append_service_arg(self, arg, kwargs):
        service_args = kwargs.get('service_args', [])
        service_args.append(arg)
        kwargs['service_args'] = service_args

    @synchronized(_methods_lock)
    def acquire_driver(self, level, browser_name, context_name):
        logger.debug('Acquiring driver %s level %s', browser_name, level)
        self.init_level(level, browser_name, context_name)
        wdriver = self.get_available_set(browser_name, context_name).pop()
        # Keep track of acquired webdrivers in case we need to close them
        self._locked.add(wdriver)
        self._released.remove(wdriver)
        return wdriver

    @synchronized(_methods_lock)
    def release_driver(self, wdriver, level):
        '''
        Release passed webdriver instance, so it becomes available to be used
        by another test. (this function is not generally used directly)
        :param wdriver: webdriver instance to be released
        :param level: level at wich we are releasing the webdriver
        '''
        logger.debug(f'Releasing {wdriver} level {level}')
        assert wdriver in self._locked, f'Webdriver {wdriver} was never locked'
        self._locked.remove(wdriver)
        cfg = self._wdriver_pool[wdriver]
        if cfg.shared:
            # Make sure we release context_name
            for context_name, lvl in self._context_name_level.copy().items():
                if lvl == level:
                    del self._context_name_level[context_name]
        # Make sure webdriver is healthy and from the right level
        # before reusing it
        if not self._quit_failed_webdriver(wdriver):
            # Keep webdriver with higher level of life
            self._released.add(wdriver)

    @synchronized(_methods_lock)
    def quit_all_webdrivers(self):
        for wdriver in self._wdriver_pool:
            self._quit_webdriver(wdriver)
        self._wdriver_pool.clear()
        self._locked.clear()
        self._released.clear()
        self._context_name_level.clear()

    def _quit_webdriver(self, wdriver):
        # quit a webdriver, catch any exception and report it
        try:
            self.log.d('Quitting webdriver %s', wdriver)
            wdriver.quit()
        except Exception as e:
            self.log.w('Ignoring %r:%s' % (e,e))

    @synchronized(_methods_lock)
    def quit_all_failed_webdrivers(self):
        remove = lambda s,e: e in s and s.remove(e)
        for wdriver in list(self._wdriver_pool):
            if self._quit_failed_webdriver(wdriver):
                cfg = self._wdriver_pool.pop(wdriver)
                remove(self._locked, wdriver)
                remove(self._released, wdriver)
                if cfg.context in self._context_name_level:
                    del self._context_name_level[cfg.context]

    def _quit_failed_webdriver(self, wdriver):
        failed = self._is_failed_webdriver(wdriver)
        if failed:
            self._quit_webdriver(wdriver)
            return failed

    def _is_failed_webdriver(self, wdriver, tested_once=False):
        # Test wether a webdriver is responding, if not quit it and
        # unregister it to avoid further usage.
        try:
            wdriver.current_url
            return False
        except UnexpectedAlertPresentException as e:
            # An alert window will cause an exception, handle it only once
            alert = wdriver.switch_to_alert()
            alert.accept()
            if not tested_once:
                return self._is_failed_webdriver(wdriver, tested_once=True)
            # We were unable to determine it
            raise
        except Exception as e:
            return e
        return True

    @synchronized(_methods_lock)
    def start_display(self):
        '''
        Create virtual display if set by configuration
        '''
        def get(name, default=None):
            return self.global_settings.get('virtual_display_' + name, default)
        if get('enabled') and not self._virtual_display:
            # We need to setup a new virtual display
            kwargs = get('backend_kwargs') or {}
            display = Display(backend=get('backend'), size=get('size', (800, 600)),
                    visible=get('visible'), **kwargs)
            self.log.d('Starting virtual display %r', display)
            display.start()
            self._virtual_display = display

    @synchronized(_methods_lock)
    def stop_display(self):
        '''
        Convenient function to stop the virtual display
        '''
        # Nice alias
        display = self._virtual_display
        if ((not self.global_settings.get('virtual_display_keep_open')
             or not self.global_settings.get('virtual_display_visible'))
                and display):
            self.log.d('Stopping virtual display %r', display)
            display.stop()
            self._virtual_display = None

    @synchronized(_methods_lock)
    def list_webdrivers(self, which='all'):
        '''
        Make a report of all, released or locked webdrivers.
        :param which: string specifiying the type of report. May be:'all', 'released', 'locked'
        '''
        wdrivers_report = {}
        possible = ('all', 'released', 'locked')
        assert which in possible, 'Which must be one of %r' % possible
        # Choose the set to report
        if which =='all':
            in_report = self._wdriver_pool
        elif which == 'released':
            in_report = self._released
        elif which == 'locked':
            in_report = self._locked
        # Build report
        for wdriver in in_report:
            wdrivers_report[wdriver] = self._wdriver_pool[wdriver]
        return wdrivers_report

    def get_browser_name(self, browser_name=None):
        '''
        Get the current browser name in usage
        If not set, we use the one specified in global settings
        or PhantomJS as the final default
        '''
        browser = (browser_name
                   or self.global_settings.get('webdriver_browser'))
        return self.expand_browser_name(browser)

    def expand_browser_name(self, browser=None):
        '''
        Expand a partial or lower case Browser's name into its full name.
        Eg:
            firefo -> Firefox
            chrom -> Chrome
        :param browser: partial browser's name string
        '''
        # TODO: add IE and Opera
        char_browser = dict(f='Firefox',
                            c='Chrome',
                            p='PhantomJS',
                            )
        char = browser.lower()[0]
        assert char in char_browser, 'Could not find browser %r' % browser
        return char_browser.get(char)

    def __del__(self):
        self.exit_level(MANAGER_LIFE)
        self.stop_display()


class BrowserContextManager(XpathWdBase):
    def __init__(self, parent, level, base_url=None, context_name='', browser_name=None):
        self.parent = parent
        self.level = level
        self.base_url = base_url
        self.name = context_name
        self.webdriver = None
        self.browser_name = browser_name
        
    def __enter__(self):
        return self.get_xpathbrowser()
    
    def __exit__(self, type=None, value=None, traceback=None):
        # save screenshot if exception
        self.release_driver()
        self.parent.exit_level(self.level)

    def acquire_driver(self):
        if not self.webdriver:
            self.webdriver = self.parent.acquire_driver(self.level, self.browser_name, self.name)
        return self.webdriver

    def get_xpathbrowser(self, base_url=None, name=''):
        from .logger import Logger
        from .xpath_browser import XpathBrowser
        base_url = base_url or self.base_url or self.global_settings.get('base_url')
        name = name or self.name
        # Initialize the XpathBrowser class
        return XpathBrowser(self.acquire_driver(), base_url,
                            Logger(name), settings=self.global_settings)

    def release_driver(self):
        if self.webdriver:
            self.parent.release_driver(self.webdriver, self.level)
            self.webdriver = None


def get_browser(context_name='default', browser=None):
    '''
    :param name: optional context's name (mainly for logging purposes)
    :param browser: optional browser name string (eg: 'Firefox', 'Chrome', 'PhantomJs')
    '''
    return WebdriverManager().get_browser(context_name, browser)


def smoke_test_module():
    from .logger import log_test
    mngr = WebdriverManager()
#    import ipdb; ipdb.set_trace()
    lvl = mngr.enter_level(level=TEST_ROUND_LIFE)
    wd = lvl.acquire_driver()
    log_test(wd)
    lvl.release_driver()
    log_test(mngr.list_webdrivers())
#    import ipdb; ipdb.set_trace()
    xb = lvl.get_xpathbrowser()
    log_test(xb)
    lvl.exit_level()
#    import ipdb; ipdb.set_trace()
    mngr.stop_display()
    mngr.quit_all_webdrivers()
    # Wait some time for browser to quit
    import time
    time.sleep(.5)


if __name__ == "__main__":
    smoke_test_module()
