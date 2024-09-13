#!/bin/bash

set -e -x


sudo apt-get install -y imagemagick findimagedupes xvfb chromium-browser chromium-chromedriver

pip3 install -r requirements.tests.txt
pip3 install -r requirements.txt

export \
XPATHWD_VIRTUAL_DISPLAY_ENABLED=True \
XPATHWD_VIRTUAL_DISPLAY_VISIBLE=False

bash run_tests.sh