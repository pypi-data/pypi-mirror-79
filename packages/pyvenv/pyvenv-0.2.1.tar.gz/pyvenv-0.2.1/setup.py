# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvenv']

package_data = \
{'': ['*']}

install_requires = \
['clipboard>=0.0.4,<0.0.5', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['pyvenv = pyvenv.main:main']}

setup_kwargs = {
    'name': 'pyvenv',
    'version': '0.2.1',
    'description': 'A minimalist python environment manager.',
    'long_description': "# PyVenv\n---\n> A minimalist python environment manager.\n```\n\n ____      __     __              \n|  _ \\ _   \\ \\   / /__ _ ____   __\n| |_) | | | \\ \\ / / _ \\ '_ \\ \\ / /\n|  __/| |_| |\\ V /  __/ | | \\ V / \n|_|    \\__, | \\_/ \\___|_| |_|\\_/  \n       |___/                      \n\nhelp: pyvenv <command> [arguments]\n\nGlobal Options:\n    -h, --help               Show this help message and exit.\n    \nCommands:\n    \n    create                   Create a new environment.\n        Options: pyvenv create <environment name>\n\n    remove                   Delete an environment.\n        Options: pyvenv remove <environment name>\n\n    shell                    Activate an environment.\n        Options: pyvenv activate <environment name>\n\n\n```\n",
    'author': 'Ashrit Yarava',
    'author_email': 'ashdragon95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ashrit-Yarava/pyvenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
