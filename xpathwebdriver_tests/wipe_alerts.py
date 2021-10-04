from xpathwebdriver_tests.test_XpathBrowser import WebUnitTestBase
import unittest


class TestXpathBrowserWipeAlerts(WebUnitTestBase):
    def test_wipe_alerts(self):
        from selenium.common.exceptions import UnexpectedAlertPresentException
        body = '''
          <script type="text/javascript">
            alert('Example alert');
          </script>
        '''
        try:
            with self.create_html('test_wipe_alerts', body) as path:
                self.get_local_page(path)
        except UnexpectedAlertPresentException:
            self.browser.wipe_alerts()
        else:
            self.fail('No alert wiped')

if __name__ == "__main__":
    unittest.main()
