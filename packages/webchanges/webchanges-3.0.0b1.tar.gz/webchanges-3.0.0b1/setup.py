#!/usr/bin/env python3

# this is run by pip or Docker to install the project

import os
import re
import sys

from setuptools import setup

import webchanges as project

project_name = project.__project_name__

if sys.version_info < project.__min_python_version__:
    sys.exit(f'{project_name} requires Python version {".".join(str(v) for v in project.__min_python_version__)} or newer.\n'
             f'You are running {sys.version}')

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open('README.rst') as f:
    README_rst = f.read()

SETUP = {
    'name': project.__project_name__,
    'version': project.__version__,
    'description': project.__doc__.strip().split('\n\n', 1)[0],
    'long_description': README_rst,
    'long_description_content_type': 'text/x-rst',
    'author': re.match(r'(.*) <(.*)>', project.__author__).groups()[0],
    'author_email': re.match(r'(.*) <(.*)>', project.__author__).groups()[1],
    'url': project.__url__,
    'packages': [project_name],
    'classifiers': ['Environment :: Console',
                    'Topic :: Internet',
                    'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
                    'Topic :: Utilities',
                    'Development Status :: 5 - Production/Stable',
                    'License :: OSI Approved :: MIT License',
                    'License :: OSI Approved :: BSD License',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3 :: Only',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python :: 3.8',
                    'Programming Language :: Python :: 3.9',
                    'Operating System :: OS Independent',
                    'Natural Language :: English',
                    'Intended Audience :: Developers',
                    'Intended Audience :: End Users/Desktop',
                    'Intended Audience :: System Administrators'],
    'license': project.__license__,
    # 'license_file': 'LICENSE',
    # data_files is deprecated. It does not work with wheels, so it should be avoided.
    'package_dir': {'': '.'},
    'install_requires': requirements if os.name != 'nt' else requirements.extend(['colorama']),
    'entry_points': {'console_scripts': [f'{project_name}={project_name}.cli:main']},
    'extras_require': {'use_browser':  ['pyppeteer'],
                       'beautify': ['beautifulsoup4', 'jsbeautifier', 'cssbeautifier'],
                       'bs4': ['beautifulsoup4'],
                       'pdf2text': ['pdftotext'],
                       'ical2text': ['vobject'],
                       'ocr': ['pytesseract', 'Pillow'],
                       'pushover': ['chump'],
                       'pushbullet': ['pushbullet.py'],
                       'matrix': ['matrix_client'],
                       'xmpp': ['aioxmpp'],
                       'safe_password': ['keyring'],
                       'redis': ['redis', 'msgpack'],
                       'developer': ['flake8', 'flake8-import-order', 'pytest', 'docutils', 'sphynx',
                                     'sphinx_rtd_theme']},
    'python_requires': f'>={".".join(str(v) for v in project.__min_python_version__)}',
    'project_urls': {'Bug Tracker': f'{project.__url__.rstrip("//")}/issues',
                     'Source Code': project.__url__,
                     'Documentation': f'https://{project_name}.readthedocs.io/en/stable/'}}
SETUP['extras_require']['all'] = [pkg for extra in SETUP['extras_require'].values() for pkg in extra]

setup(**SETUP)


# to build docs
# argparse-manpage --pyfile ./pythonfile --function get_parser > cool-manpage.1

# to build (https://packaging.python.org/tutorials/packaging-projects/):
# python setup.py sdist bdist_wheel
# python -m twine upload --repository testpypi dist/*