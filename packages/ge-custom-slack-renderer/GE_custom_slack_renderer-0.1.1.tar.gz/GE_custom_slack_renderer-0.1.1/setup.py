# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ge_custom_slack_renderer']

package_data = \
{'': ['*']}

install_requires = \
['great_expectations>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'ge-custom-slack-renderer',
    'version': '0.1.1',
    'description': 'Complement library to customize Great Expectations Slack notifications',
    'long_description': None,
    'author': 'Eli Pino',
    'author_email': 'elisabet.pino@glovoapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
