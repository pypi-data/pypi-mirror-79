# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsc', 'gsc.exercises']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'requests>=2.24.0,<3.0.0',
 'typer>=0.1.1,<0.2.0',
 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['gsc = gsc.cli:main']}

setup_kwargs = {
    'name': 'gsc',
    'version': '2.0.3',
    'description': 'Git for Scientists practical exercise helper.',
    'long_description': '# gsc\n\n![build](https://github.com/git-scientist/gsc/workflows/build/badge.svg)\n\nGit for Scientists practical exercise helper.\n\nSee https://www.gitscientist.com for more.\n',
    'author': 'Daniel Tipping',
    'author_email': 'daniel@gitscientist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.gitscientist.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
