#!/bin/bash

pushd `dirname $0` > /dev/null
    #pip install -r requirements.txt
    python -m unittest discover -s xpathwebdriver_tests
    python examples/01_duckduckgo_basic.py
    python examples/03_new_browser_per_test.py
    python examples/04_mutiple_browsers.py
popd > /dev/null
