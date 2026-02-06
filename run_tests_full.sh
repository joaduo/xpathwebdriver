#!/bin/bash

set -e -x

pushd `dirname $0` > /dev/null
    export PYTHONPATH="$PYTHONPATH:./"
    bash run_tests.sh
    echo "Also running examples"
    python3 examples/01_duckduckgo_basic.py
    python3 examples/03_new_browser_per_test.py
    python3 examples/04_mutiple_browsers.py
popd > /dev/null
