#!/bin/bash

set -e -x

export PYTHONPATH="$PYTHONPATH:./"

pushd `dirname $0` > /dev/null
    if ! [ "$(uname)" = "Darwin" ]; then
        python3 xpathwebdriver_tests/test_ImagesComparator.py
    fi
popd > /dev/null

pushd `dirname $0` > /dev/null
    python3 xpathwebdriver_tests/test_XPathBrowser.py
    python3 xpathwebdriver_tests/wipe_alerts.py
popd > /dev/null
