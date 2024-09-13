#!/bin/bash

sudo apt-get install -y findimagedupes
pip install -r requirements.tests.txt
pip install -r requirements.txt

bash run_tests.sh
