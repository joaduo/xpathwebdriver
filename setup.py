
from setuptools import setup, find_packages

name = 'xpathwebdriver'

reqs = '''importlib
ipython
pyvirtualdisplay
selenium
rel_imp'''.splitlines()

def long_description():
    with open('README', 'r') as f:
        return unicode(f.read())

setup(
  name = name,
  packages = find_packages(),
  version = '0.1.5',
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
