
from setuptools import setup, find_packages

name = 'xpathwebdriver'

reqs = '''importlib>=1.0.4
ipython>=5.1.0
pyvirtualdisplay>=0.2.1
selenium>=3.0.2
rel_imp>=0.2.4'''.splitlines()

def long_description():
    with open('README', 'r') as f:
        return unicode(f.read())

setup(
  name = name,
  packages = find_packages(),
  version = '0.2.0',
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
