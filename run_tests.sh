#!/bin/bash

set -e -x

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$SCRIPT_DIR/test.sh"

if ! [ "$(uname)" = "Darwin" ]; then
    $RUNNER xpathwebdriver_tests/test_ImagesComparator.py
fi

$RUNNER xpathwebdriver_tests/test_XpathBrowser.py
$RUNNER xpathwebdriver_tests/wipe_alerts.py
$RUNNER xpathwebdriver_tests/test_01_duckduckgo_basic.py
$RUNNER xpathwebdriver_tests/test_03_new_browser_per_test.py
$RUNNER xpathwebdriver_tests/test_04_mutiple_browsers.py
$RUNNER xpathwebdriver_tests/test_XpathBrowser_extended.py
$RUNNER xpathwebdriver_tests/test_WebdrivrManager_browser_options.py
