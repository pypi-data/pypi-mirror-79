# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['kerdokustats']
install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'kerdokustats',
    'version': '1.0.4.1',
    'description': 'KerdokuBot Stats',
    'long_description': '**KerdokuBot Stats Package.**\n\n**Installation** \\\nTo install KerdokuStats:\\\n```$ pip install kerdokustats```\n\n\n**Example code:**\n\n```py\nimport kerdokustats\n\nguilds = kerdoku().guilds #Show bot guilds count\nusers = kerdoku().users #Show bot users count\ntime = kerdoku().time #Show bot LSRT\n\nprint(guilds)\nprint(users)\nprint(time)\n```\n\nIf you have a question or idea, go to KerdokuBot technical support server. https://kerdokuds.ml\n\n',
    'author': 'Grey Cat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kerdokuds.ml',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
