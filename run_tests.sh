#!/bin/bash

pushd `dirname $0` > /dev/null
    #pip install -r requirements.txt
    python -m unittest discover -s xpathwebdriver_tests
popd > /dev/null
