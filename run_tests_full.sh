#!/bin/bash

set -e -x

pushd `dirname $0` > /dev/null
    python3 -m unittest discover -s xpathwebdriver_tests
    python3 xpathwebdriver_tests/wipe_alerts.py #fails miserably on PhantomJs in Codeship
    echo "Also running examples"
    python3 examples/01_duckduckgo_basic.py
    python3 examples/03_new_browser_per_test.py
    python3 examples/04_mutiple_browsers.py
popd > /dev/null
