# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nitter_scraper']

package_data = \
{'': ['*'], 'nitter_scraper': ['templates/*']}

install_requires = \
['docker>=4.3.1,<5.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'loguru>=0.5.1,<0.6.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'nitter-scraper',
    'version': '0.3.2',
    'description': 'Scrape Twitter API without authentication using Nitter.',
    'long_description': None,
    'author': 'dgnsrekt',
    'author_email': 'dgnsrekt@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
