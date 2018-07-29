'''
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()

from selenium import webdriver
from pyvirtualdisplay import Display
from threading import RLock
from functools import wraps
from selenium.common.exceptions import UnexpectedAlertPresentException
from .base import XpathWdBase, singleton_decorator
from .solve_settings import solve_settings
from xpathwebdriver.levels import INMORTAL_LIFE, TEST_ROUND_LIFE
import os


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


@singleton_decorator
class WebdriverManager(XpathWdBase):
    '''
    This is a "Context Manager" for the Webdriver's instances available. (used
    for running tests in general)
    '''
    # Thread lock for methods in this class
    _methods_lock = RLock()

    def __init__(self):
        # Set of locked webdrivers
        self._locked = set()
        # Set of released webdrivers
        self._released = set()
        # Pool of drivers {wdriver:(browser_name, driver_life_level)}
        self._wdriver_pool = {}
        # Virtual display object where we start webdrivers
        self._virtual_display = None
        # Current selected browser
        self._browser_name = None

    @property
    def enabled(self):
        return solve_settings().get('webdriver_enabled')

    @synchronized(_methods_lock)
    def release_driver(self, wdriver, level):
        '''
        Release passed webdriver instance, so it becomes available to be used
        by another test. (this function is not generally used directly)
        :param wdriver: webdriver instance to be released
        :param level: level at wich we are releasing the webdriver
        '''
        if not wdriver:
            return
        assert wdriver in self._locked, 'Webdriver %r was never locked' % wdriver
        self._locked.remove(wdriver)
        _, drv_level = self._wdriver_pool[wdriver]
        # Make sure webdriver is healthy and from the right level
        # before reusing it
        if drv_level >= level and not self._quit_failed_webdriver(wdriver):
            # Keep webdriver with higher level of life
            self._released.add(wdriver)
        else:
            # Remove no longer needed webdriver
            self._quit_webdriver(wdriver)

    def _quit_failed_webdriver(self, wdriver, tested_once=False):
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
                return self._quit_failed_webdriver(wdriver, tested_once=True)
        except Exception as e:
            self.log.e('Quitting webdriver %r due to exception %r:%s' %
                       (wdriver, e, e))
        self._quit_webdriver(wdriver)
        return True

    def _quit_webdriver(self, wdriver):
        # quit a webdriver, catch any exception and report it
        try:
            wdriver.quit()
        except Exception as e:
            self.log.w('Ignoring %r:%s' % (e,e))

    @synchronized(_methods_lock)
    def init_level(self, level):
        '''
        Initialize webdriver for a specific Life Level.
        There are two possibilities:
          1- no webdriver was initialized on previous level => init it 
          2- there is a webdriver for the browser selected, no action is performed.
        :param level: webdriver's level of life we are entering
        '''
        if not self.enabled:
            return
        # level is mandatory
        assert 0 < level < INMORTAL_LIFE, 'No process level set'
        # Get rid of non-responding browsers
        self.quit_all_failed_webdrivers()
        # Get the set of released webdrivers for the selected browser
        released = self.get_available_set()
        # If no webdriver available, then create a new one 
        if not released:
            # Create webdriver if needed
            browser = self.get_browser_name()
            wdriver = self._new_webdriver(browser)
            self._wdriver_pool[wdriver] = browser, level
            self._released.add(wdriver)

    @synchronized(_methods_lock)
    def get_available_set(self):
        '''
        Return the set of avialable webdrivers for the current Browser selected
        (in global configuration)
        '''
        browser = self.get_browser_name()
        browser_set = set([wdriver
                           for wdriver,(brws,_) in self._wdriver_pool.items()
                           if brws == browser])
        return (self._released & browser_set)

    @synchronized(_methods_lock)
    def exit_level(self, level):
        def common(wdriver, container):
            _, drv_level = self._wdriver_pool[wdriver]
            if self._quit_failed_webdriver(wdriver):
                container.remove(wdriver)
                self._wdriver_pool.pop(wdriver)
            elif drv_level <= level:
                container.remove(wdriver)
                self._quit_webdriver(wdriver)
                self._wdriver_pool.pop(wdriver)
        # Make copies of sets, we are going to modify them
        for wdriver in self._released.copy():
            common(wdriver, self._released)
        for wdriver in self._locked.copy():
            common(wdriver, self._locked)

    @synchronized(_methods_lock)
    def acquire_driver(self, level):
        if not self.enabled:
            return None
        self.init_level(level)
        wdriver = self.get_available_set().pop()
        # Keep track of acquired webdrivers in case we need to close them
        self._locked.add(wdriver)
        self._released.remove(wdriver)
        return wdriver

    def _new_webdriver(self, browser=None, *args, **kwargs):
        browser = self.expand_browser_name(browser)
        # Setup display before creating the browser
        self.setup_display()
        def append_service_arg(arg):
            service_args = kwargs.get('service_args', [])
            service_args.append(arg)
            kwargs['service_args'] = service_args
        if browser == 'PhantomJS':
            append_service_arg('--ignore-ssl-errors=true')
        if (browser == 'Firefox'
        and self.global_settings.get('webdriver_firefox_profile')
        and not args and not kwargs.has_key('firefox_profile')):
            # Update with profile specified from config
            fp = webdriver.FirefoxProfile(self.global_settings.get('webdriver_firefox_profile'))
            kwargs['firefox_profile'] = fp
        if (browser == 'Chrome' and os.name == 'posix' and os.geteuid() == 0):
            self.log.w('Passing --no-sandbox flag to Chrome (running as root)')
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            #self.log.w('Adding --disable-application-cache')
            #chrome_options.add_argument('--disable-application-cache')
            #chrome_options.add_argument('--incognito')
            kwargs['chrome_options'] = chrome_options
        driver = getattr(webdriver, browser)(*args, **kwargs)
        return driver

    @synchronized(_methods_lock)
    def quit_all_webdrivers(self):
        for wdriver in self._wdriver_pool:
            self._quit_webdriver(wdriver)
        self._wdriver_pool.clear()
        self._locked.clear()
        self._released.clear()

    @synchronized(_methods_lock)
    def quit_all_failed_webdrivers(self):
        found_one = False
        remove = lambda s,e: e in s and s.remove(e)
        for wdriver in self._wdriver_pool.keys():
            if self._quit_failed_webdriver(wdriver):
                self._wdriver_pool.pop(wdriver)
                remove(self._locked, wdriver)
                remove(self._released, wdriver)
                found_one = True
        return found_one

    @synchronized(_methods_lock)
    def setup_display(self):
        '''
        Create virtual display if set by configuration
        '''
        def get(name, default=None):
            return self.global_settings.get('virtual_display_' + name, default)
        if not get('enable'):
            if self._virtual_display:
                self.log.w('There is a display enabled although config says'
                           ' different')
            return
        elif self._virtual_display:
            # There is a display configured
            return
        # We need to setup a new virtual display
        d = Display(backend=get('backend'), size=get('size', (800, 600)),
                visible=get('visible'))
        d.start()
        self._virtual_display = d

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
            self.log.d('Stopping virtual display %r' % display)
            display.stop()
            WebdriverManager._virtual_display = None

    @synchronized(_methods_lock)
    def enter_level(self, level, base_url=None, name=''):
        return WebdriverLevelManager(self, level, base_url, name)

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
            browser, level = self._wdriver_pool[wdriver]
            wdrivers_report[wdriver] = browser, level
        return wdrivers_report

    @synchronized(_methods_lock)
    def set_browser(self, browser):
        '''
        :param browser: browser's name string
        '''
        assert browser
        self._browser_name = browser

    def get_browser_name(self):
        '''
        Get the current browser name in usage
        If not set, we use the one specified in global settings
        or PhantomJS as the final default
        '''
        browser = (self._browser_name
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


class WebdriverLevelManager(XpathWdBase):
    def __init__(self, parent, level, base_url=None, name=''):
        self.parent = parent
        self.level = level
        self.base_url = base_url
        self.name = name
        self.webdriver = None
        self.parent.init_level(self.level)
        
    def __enter__(self):
        return self.get_xpathbrowser()
    
    def __exit__(self, type, value, traceback):
        self.exit_level()

    def get_locked_driver(self):
        return self.webdriver

    def acquire_driver(self):
        assert not self.webdriver, 'Webdriver already acquired'
        self.webdriver = self.parent.acquire_driver(self.level)
        return self.webdriver

    def get_xpathbrowser(self, base_url=None, name=''):
        from .logger import Logger
        from .xpath_browser import XpathBrowser
        base_url = base_url or self.base_url or self.global_settings.get('base_url')
        name = name or self.name
        # Initialize the XpathBrowser class
        return XpathBrowser(self.acquire_driver(), base_url,
                            Logger(name), settings={})

    def exit_level(self):
        self.release_driver()
        self.parent.exit_level(self.level)

    def release_driver(self):
        if self.webdriver:
            self.parent.release_driver(self.webdriver, self.level)
            self.webdriver = None


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
