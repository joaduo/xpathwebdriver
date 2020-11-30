#!/bin/bash
if ! pandoc --from=markdown --to=rst --output=README README.md ; then
    echo "pandoc command failed. Probably it is not installed. Aborting."
    exit 1
fi

app="xpathwebdriver"

rm dist/$app\-*.tar.gz

pip install twine

python setup.py sdist && twine check dist/$app\-*.tar.gz

function test_venv(){
    #test installation
    mkdir venv -p
    cd venv
    virtualenv -p python3 ./
    source bin/activate
    pip install ../dist/$app\-*.tar.gz
    pip uninstall $app -y
    cd ..
    #rm venv -Rf
}

function full_tests(){
    echo WIP
}

if [ "$1" == "venv" ] ;  then
test_venv
elif [ "$1" == "full" ] ;  then
test_venv
full_tests
fi

pkg=`ls dist/$app\-*.tar.gz`
echo
echo "upload with: twine upload $pkg"
