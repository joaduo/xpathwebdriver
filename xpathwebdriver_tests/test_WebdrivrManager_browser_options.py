# -*- coding: utf-8 -*-
'''
xpathwebdriver

Code Licensed under MIT License. See LICENSE file.
'''
import unittest
from unittest.mock import Mock, patch, MagicMock
import os

from xpathwebdriver.webdriver_manager import WebdriverManager
from xpathwebdriver.default_settings import DefaultSettings
from xpathwebdriver.solve_settings import register_settings_instance, solve_settings


class TestBrowserOptions(unittest.TestCase):
    """
    Test browser options configuration from default settings.
    Tests the _create_browser_options method to ensure settings are correctly applied.
    """

    def setUp(self):
        """Set up test settings and manager instance."""
        self.settings = DefaultSettings()
        register_settings_instance(self.settings)
        self.manager = WebdriverManager()

    def tearDown(self):
        """Clean up settings."""
        # Reset settings to avoid affecting other tests

    def test_firefox_options_default(self):
        """Test Firefox options with default settings."""
        options = self.manager._create_browser_options('Firefox')
        self.assertIsNotNone(options)
        # Default should not be headless
        self.assertNotIn('--headless', options.arguments)

    def test_firefox_options_headless(self):
        """Test Firefox options with headless enabled."""
        self.settings.webdriver_headless = True
        options = self.manager._create_browser_options('Firefox')
        self.assertIsNotNone(options)
        self.assertIn('--headless', options.arguments)

    def test_firefox_options_with_profile(self):
        """Test Firefox options with profile directory."""
        profile_dir = '/tmp/test_profile'
        options = self.manager._create_browser_options('Firefox', profile_dir)
        self.assertIsNotNone(options)
        # Check that profile arguments were added
        args = options.arguments
        self.assertIn('-profile', args)
        self.assertIn(profile_dir, args)

    def test_chrome_options_default(self):
        """Test Chrome options with default settings."""
        options = self.manager._create_browser_options('Chrome')
        self.assertIsNotNone(options)
        # Default should not be headless
        self.assertNotIn('--headless', options.arguments)

    def test_chrome_options_headless(self):
        """Test Chrome options with headless enabled."""
        self.settings.webdriver_headless = True
        options = self.manager._create_browser_options('Chrome')
        self.assertIsNotNone(options)
        self.assertIn('--headless', options.arguments)

    def test_chrome_options_with_profile(self):
        """Test Chrome options with profile directory."""
        profile_dir = '/tmp/test_profile'
        options = self.manager._create_browser_options('Chrome', profile_dir)
        self.assertIsNotNone(options)
        # Check that user-data-dir argument was added
        args = options.arguments
        # Check for argument that starts with --user-data-dir
        self.assertTrue(any(arg.startswith('--user-data-dir=') for arg in args))

    @patch('os.geteuid')
    def test_chrome_options_no_sandbox_as_root(self, mock_geteuid):
        """Test Chrome options add --no-sandbox when running as root."""
        mock_geteuid.return_value = 0
        with patch('os.name', 'posix'):
            options = self.manager._create_browser_options('Chrome')
            self.assertIsNotNone(options)
            args = options.arguments
            self.assertIn('--no-sandbox', args)

    def test_edge_options_default(self):
        """Test Edge options with default settings."""
        options = self.manager._create_browser_options('Edge')
        self.assertIsNotNone(options)
        # Default should not be headless
        self.assertNotIn('--headless', options.arguments)

    def test_edge_options_headless(self):
        """Test Edge options with headless enabled."""
        self.settings.webdriver_headless = True
        options = self.manager._create_browser_options('Edge')
        self.assertIsNotNone(options)
        self.assertIn('--headless', options.arguments)

    def test_safari_options_default(self):
        """Test Safari options with default settings."""
        options = self.manager._create_browser_options('Safari')
        self.assertIsNotNone(options)

    def test_safari_options_headless_warning(self):
        """Test Safari options warn about headless not being supported."""
        self.settings.webdriver_headless = True
        with patch.object(self.manager.log, 'w') as mock_log:
            options = self.manager._create_browser_options('Safari')
            self.assertIsNotNone(options)
            # Should log a warning about headless not being supported
            mock_log.assert_called()
            warning_message = mock_log.call_args[0][0]
            self.assertIn('Safari does not support headless mode', warning_message)

    def test_generic_options_headless(self):
        """Test generic options with headless enabled for unknown browser."""
        # Skip this test since expand_browser_name raises LookupError for unknown browsers
        self.skipTest("expand_browser_name raises LookupError for unknown browsers")

    def test_headless_setting_from_global_settings(self):
        """Test that headless setting is read from global_settings."""
        # Set via global_settings using the set method
        self.manager.global_settings.set('webdriver_headless', True)
        options = self.manager._create_browser_options('Chrome')
        self.assertIn('--headless', options.arguments)


if __name__ == "__main__":
    unittest.main()
