from setuptools import setup, find_packages


name = 'xpathwebdriver'

reqs = '''pyvirtualdisplay>=0.2.1
selenium>=3.0.2
parsel>=1.6.0'''.splitlines()


def long_description():
    with open('README', 'r') as f:
        return f.read()


setup(
  name = name,
  packages = find_packages(),
  version = '2.0.6',
  description = 'Selenium/webdriver wrapper for XPath and CSS selection',
  long_description=long_description(),
  long_description_content_type='text/x-rst',
  author = 'Joaquin Duo',
  author_email = 'joaduo@gmail.com',
  license='MIT',
  url = 'https://github.com/joaduo/'+name,
  keywords = ['testing', 'automation', 'web', 'unittest', 'webdriver', 'selenium', 'xpath', 'css'],
  install_requires=reqs,
  scripts=[
           'xpathwebdriver/commands/xpathshell',
           ],
)
