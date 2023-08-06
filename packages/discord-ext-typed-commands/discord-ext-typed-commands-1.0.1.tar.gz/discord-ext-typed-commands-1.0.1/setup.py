# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord', 'discord.ext.typed_commands', 'tests']

package_data = \
{'': ['*']}

modules = \
['mypy']
install_requires = \
['discord.py>=1.4.1,<2.0.0', 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'discord-ext-typed-commands',
    'version': '1.0.1',
    'description': 'Typed commands for discord.py',
    'long_description': '# discord-ext-typed-commands\n\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/bryanforbes/discord-ext-typed-commands/blob/master/LICENSE)\n[![Unit tests](https://github.com/bryanforbes/discord-ext-typed-commands/workflows/Unit%20tests/badge.svg)](https://github.com/bryanforbes/discord-ext-typed-commands/actions?query=workflow%3A%22Unit+tests%22)\n[![CodeQL Analysis](https://github.com/bryanforbes/discord-ext-typed-commands/workflows/CodeQL%20Analysis/badge.svg)](https://github.com/bryanforbes/discord-ext-typed-commands/actions?query=workflow%3A%22CodeQL+Analysis%22)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nThis package contains a discord.py extension to provide classes to more easily use typed commands\n\n## Installation\n\n```\npip install discord-ext-typed-commands\n```\n\n**NOTE:** Because `discord.py` uses namespace packages for its extensions, `mypy` must be configured to use namespace packages either with the `--namespace-packages` command line flag, or by setting `namespace_packages = True` in your `mypy` configuration file. See the [import discovery](https://mypy.readthedocs.io/en/stable/command_line.html#import-discovery) section of the `mypy` documentation for more details.\n\n## Development\n\nMake sure you have [poetry](https://python-poetry.org/) installed.\n\n```\npoetry install\npoetry run pre-commit install --hook-type pre-commit --hook-type post-checkout\n```\n',
    'author': 'Bryan Forbes',
    'author_email': 'bryan@reigndropsfall.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bryanforbes/discord-ext-typed-commands',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
