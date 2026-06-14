#!/bin/bash

set -e -x



sudo apt-get install -y imagemagick findimagedupes xvfb chromium-browser 2>&1 > installation.txt
# chromium-chromedriver (unneeded and breaks things!)

tail -n 100 installation.txt

pip3 install -r requirements.tests.txt
pip3 install -r requirements.txt


cat /etc/lsb-release
whereis chromium.chromedriver
which chromium.chromedriver

export \
XPATHWD_VIRTUAL_DISPLAY_ENABLED=True \
XPATHWD_VIRTUAL_DISPLAY_VISIBLE=False

bash run_tests.sh
