#!/bin/bash

set -e -x

pushd `dirname $0` > /dev/null
    python -m unittest discover -s xpathwebdriver_tests
    python xpathwebdriver_tests/wipe_alerts.py
popd > /dev/null
