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
    'version': '1.0.0',
    'description': 'PyQT SQL executor demo example using DB API (no QtSQL)',
    'long_description': None,
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
