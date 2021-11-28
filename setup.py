from setuptools import setup, find_packages


name = 'xpathwebdriver'

reqs = '''pyvirtualdisplay>=0.2.1
selenium>=3.0.2
rel_imp>=0.2.4'''.splitlines()


def long_description():
    with open('README', 'r') as f:
        return f.read()


setup(
  name = name,
  packages = find_packages(),
  version = '2.0.3',
  description = 'Simpler selenium/webdriver API through a wrapper',
  long_description=long_description(),
  long_description_content_type='text/x-rst',
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
