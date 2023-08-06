# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqt_sql_demo',
 'pyqt_sql_demo.connection',
 'pyqt_sql_demo.syntax_highlighter',
 'pyqt_sql_demo.widgets']

package_data = \
{'': ['*']}

install_requires = \
['pygments>=2.6.1,<3.0.0', 'pyqt5>=5.15.0,<6.0.0']

entry_points = \
{'console_scripts': ['pyqt-sql-demo = pyqt_sql_demo.app:launch']}

setup_kwargs = {
    'name': 'pyqt-sql-demo',
    'version': '1.0.1',
    'description': 'PyQT SQL executor demo example using DB API (no QtSQL)',
    'long_description': '# PyQT based SQL query executor demo example\n\nThis is a demo example of using PyQT and SQLite via standard Python DB-API interface. \nIt\'s created to be used as a tutorial or reference.\nIt uses `QtWidgets` for interface, `QTableView` for displaying SQL query results, `pygments` for syntax highlighting, and `sqlite3` for db connection.\n\n<p align="center">\n![PyPI - License](https://img.shields.io/pypi/l/pyqt-sql-demo?style=plastic)\n![PyPI](https://img.shields.io/pypi/v/pyqt-sql-demo?style=plastic)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyqt-sql-demo?style=plastic)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic)\n</p>\n\n![PyQt SQL Demo](docs/pyqt-sql-demo-rec.gif)\n\n## Features\n\n* Executes user\'s DDL/DML SQL queries \n* Python3, PyQt5, DB-API 2.0 (does not use QtSql!)\n* Connection string field available to user (default: local `demo.db` file)\n* Query field available to user\n* SQL syntax highlighting using `pygments` library\n* Buttons to execute or fetch query and to commit or rollback the results\n* QTableView is used to display results\n\n## Installation & Usage\n\n### Using pip (end user installation)\n\nInstall it from PyPI into your Python. This is a no-development way to install the package. An executable `pyqtsqldemo` will become available to you in your `PATH` environmental variable.\n\n```shell\n$ pip3 install pyqt-sql-demo\n```\n\nLaunch via terminal.\n\n```shell\n$ pyqt-sql-demo\n```\n\n### Using poetry (development)\n\nInstall the package into a virtual environment using Poetry.\n\n```shell\n$ poetry install\n```\n\nRun using poetry.\n\n```shell\n$ poetry run pyqt-sql-demo\n```\n\n## Development\n\n### Use pyenv\n\nI recommend installing and using `pyenv` to manage isolated Python versions on your machine that do not interfere with your system wide Python installation and with other Python versions.\nFor example, you might have Python 2.7.15 as your system default interpreter, but at the same time you need both Python 3.7.2 for some other projects and Python 3.8.5 for this project installed on the same machine. Best way to achieve this is to use `pyenv`.\n\nAfter installing `pyenv` install suitable Python version. This project was developed using Python 3.6 but was later upgraded to support latest 3.8.5.\n\n```shell\n$ pyenv install 3.8.5\n```\n\nYou\'ll notice `.pyenv-version` file in the root directory of the project, so whenever you `cd` into project directory `pyenv` will automatically start using Python version specified in that file in this directory.\n\n### Use poetry\n\nPoetry is the latest and most admirable python package manager in existence (as of 2020). This project is packed and distributed using Poetry. \n\nThe command below executed in the project\'s root directory will set up a virtual environment using current python version (system wide or the one specified using `.pyenv-version` file) and install all required dependencies into that virtual environment.\n\n```shell\n$ poetry install\n\nInstalling dependencies from lock file\n```\n\nMake modifications and run project:\n\n```shell\n$ poetry run pyqt-sql-demo\n```\n\nMake sure you run [Black](https://github.com/psf/black) to format everything properly:\n\n```shell\n$ poetry run black .\n\nAll done! ✨ 🍰 ✨\n11 files left unchanged\n```\n\nBuild project using poetry\n\n```shell\n$ poetry build\n\nBuilding pyqt-sql-demo (1.0.0)\n - Building sdist\n - Built pyqt-sql-demo-1.0.0.tar.gz\n\n - Building wheel\n - Built pyqt_sql_demo-1.0.0-py3-none-any.whl\n```\n\n## Bug reporting\n\nPlease create an issue in GitHub Issues for this project if you have a question or would like to report a bug. When reporting an issue be sure to provide as many details as possible and use proper formatting.\n\nNice details to provide when opening an issue:\n\n* Reliable way to reproduce a bug/issue\n* What was expected?\n* What you got instead?\n* What is your suggestion or clarification question?\n* Screenshots\n* Logs\n\n## License\n\nCopyright © 2020 Vagiz Duseev\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vduseev/pyqt-sql-demo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
