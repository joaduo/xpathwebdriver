import sys
from setuptools import setup, find_packages


name = 'xpathwebdriver'

reqs = '''pyvirtualdisplay>=0.2.1
selenium>=3.0.2
rel_imp>=0.2.4'''.splitlines()
if sys.version_info < (2,7):
    # importlib comes in python 2.7 and on
    reqs.append('importlib>=1.0.4')


def in_python3():
    return sys.version_info[0] > 2


def long_description():
    with open('README', 'r') as f:
        if in_python3():
            return f.read()
        else:
            return unicode(f.read())


setup(
  name = name,
  packages = find_packages(),
  version = '0.2.4',
  description = 'Simpler webdriver API through a wrapper',
  long_description=long_description(),
  author = 'Joaquin Duo',
  author_email = 'joaduo@gmail.com',
  license='MIT',
  url = 'https://github.com/joaduo/'+name,
  keywords = ['testing', 'automation', 'web', 'unittest', 'webdriver', 'selenium'],
  install_requires=reqs,
  scripts=[
           'xpathwebdriver/commands/xpathshell',
           ],
)
