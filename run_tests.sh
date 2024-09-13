#!/bin/bash

set -e -x

pushd `dirname $0` > /dev/null
    export PYTHONPATH="$PYTHONPATH:./"
    python3 -m unittest discover -s xpathwebdriver_tests
    python3 xpathwebdriver_tests/wipe_alerts.py
popd > /dev/null
