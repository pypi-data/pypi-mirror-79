# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitrate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fitrate',
    'version': '1.0.0',
    'description': 'Calculate the length of the sides that fit into the limited volume',
    'long_description': '<p align="center">\n  <img width="420px" src="https://raw.githubusercontent.com/suzukey/fitrate/main/docs/img/fitrate.png" alt=\'fitrate\'>\n</p>\n\n<p align="center">\n  <em>Calculate the length of the sides that fit into the limited volume</em>\n</p>\n\n<p align="center">\n  <a href="https://github.com/suzukey/fitrate/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/suzukey/fitrate/workflows/Test/badge.svg" alt="Test">\n  </a>\n\n  <a href="https://codecov.io/gh/suzukey/fitrate" target="_blank">\n    <img src="https://img.shields.io/codecov/c/gh/suzukey/fitrate" alt="Coverage">\n  </a>\n\n  <a href="https://pypi.org/project/fitrate/" target="_blank">\n    <img src="https://img.shields.io/pypi/v/fitrate?color=blue" alt="Package version">\n  </a>\n</p>\n\n---\n\n**Documentation**:\n\n**Demo**:\n\n---\n\n# fitrate\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```shell\n$ pip3 install fitrate\n```\n\n## Example\n\n```python\nfrom fitrate import contain\n\nprint(contain((200, 200), 60000))\n# (244, 244)\n\nprint(contain((400, 300), 60000))\n# (282, 212)\n\n# -----------\n\nfrom fitrate import scale-down\n\nprint(scale-down((200, 200), 60000))\n# (200, 200)\n\nprint(scale-down((400, 300), 60000))\n# (282, 212)\n```\n\n<p align="center">&mdash; 🎞️ &mdash;</p>\n\n<p align="center">\n  <i>fitrate is licensed under the terms of the <a href="https://github.com/suzukey/fitrate/blob/main/LICENSE">MIT license</a>.</i>\n</p>\n',
    'author': 'suzukey',
    'author_email': 'suzukei0208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/suzukey/fitrate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
