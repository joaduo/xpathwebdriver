#!/bin/bash

set -e -x

pushd `dirname $0` > /dev/null
    export PYTHONPATH="$PYTHONPATH:./"
    if ! [ "$(uname)" = "Darwin" ]; then
        python3 xpathwebdriver_tests/test_ImagesComparator.py
    fi
    python3 xpathwebdriver_tests/test_XPathBrowser.py
    python3 xpathwebdriver_tests/wipe_alerts.py
popd > /dev/null
