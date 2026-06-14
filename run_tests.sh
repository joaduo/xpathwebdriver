#!/bin/bash

set -e -x

export PYTHONPATH="$PYTHONPATH:./"

FULL_DIRECTORY="$(cd "$(dirname "$0")" && pwd)"

pushd "$FULL_DIRECTORY" > /dev/null
    if ! [ "$(uname)" = "Darwin" ]; then
        python3 xpathwebdriver_tests/test_ImagesComparator.py
    fi
    echo $(pwd)
popd > /dev/null

pushd "$FULL_DIRECTORY" > /dev/null
    ls xpathwebdriver_tests/
    python3 xpathwebdriver_tests/test_XpathBrowser.py
    python3 xpathwebdriver_tests/wipe_alerts.py
popd > /dev/null
