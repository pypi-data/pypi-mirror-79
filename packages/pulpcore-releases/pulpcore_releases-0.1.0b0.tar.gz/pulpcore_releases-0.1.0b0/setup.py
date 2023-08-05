# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pulpcore_releases']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'packaging>=20.4,<21.0']

entry_points = \
{'console_scripts': ['prc = pulpcore_releases.prc:run']}

setup_kwargs = {
    'name': 'pulpcore-releases',
    'version': '0.1.0b0',
    'description': 'Pulpcore - Releases & Compatibility',
    'long_description': 'Pulpcore - Releases & Compatibility\n-----------------------------------\n\nList the latest 3 pulpcore releases and its compatible plugins:\n\n```\n~ via 🐍 v3.8.0 (venv)\n❯ pip install pulpcore-releases\nCollecting pulpcore-releases\n  Downloading pulpcore_releases-0.1.0-py3-none-any.whl (2.7 kB)\nRequirement already satisfied: aiohttp<4.0.0,>=3.6.2 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from pulpcore-releases) (3.6.2)\nRequirement already satisfied: packaging<21.0,>=20.4 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from pulpcore-releases) (20.4)\nRequirement already satisfied: async-timeout<4.0,>=3.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (3.0.1)\nRequirement already satisfied: multidict<5.0,>=4.5 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (4.7.6)\nRequirement already satisfied: chardet<4.0,>=2.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (3.0.4)\nRequirement already satisfied: yarl<2.0,>=1.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (1.5.1)\nRequirement already satisfied: attrs>=17.3.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (20.1.0)\nRequirement already satisfied: six in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from packaging<21.0,>=20.4->pulpcore-releases) (1.15.0)\nRequirement already satisfied: pyparsing>=2.0.2 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from packaging<21.0,>=20.4->pulpcore-releases) (2.4.7)\nRequirement already satisfied: idna>=2.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from yarl<2.0,>=1.0->aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (2.10)\nInstalling collected packages: pulpcore-releases\nSuccessfully installed pulpcore-releases-0.1.0\n~ via 🐍 v3.8.0 (venv) took 2s\n❯ prc\n\nCompatible with pulpcore-3.6.3\n -> pulp-certguard-1.0.2                requirement: pulpcore<3.7,>=3.3\n -> pulp-rpm-3.6.2                      requirement: pulpcore<3.7,>=3.6\n -> pulp-cookbook-0.1.0b8               requirement: pulpcore>=3.6.0\n -> pulp-container-2.0.1                requirement: pulpcore<3.7,>=3.6\n -> pulp-file-1.2.0                     requirement: pulpcore<3.7,>=3.6\n -> pulp-ansible-0.3.0                  requirement: pulpcore<3.7,>=3.6\n -> pulp-npm-0.1.0a1.dev0               requirement: pulpcore>=3.0.0rc7\n -> pulp-deb-2.6.1                      requirement: pulpcore<3.7,>=3.6\n -> pulp-python-3.0.0b11                requirement: pulpcore>=3.6\n -> pulp-maven-0.1.0                    requirement: pulpcore>=3.1\n\nCompatible with pulpcore-3.6.2\n -> pulp-certguard-1.0.2                requirement: pulpcore<3.7,>=3.3\n -> pulp-rpm-3.6.2                      requirement: pulpcore<3.7,>=3.6\n -> pulp-cookbook-0.1.0b8               requirement: pulpcore>=3.6.0\n -> pulp-container-2.0.1                requirement: pulpcore<3.7,>=3.6\n -> pulp-file-1.2.0                     requirement: pulpcore<3.7,>=3.6\n -> pulp-ansible-0.3.0                  requirement: pulpcore<3.7,>=3.6\n -> pulp-npm-0.1.0a1.dev0               requirement: pulpcore>=3.0.0rc7\n -> pulp-deb-2.6.1                      requirement: pulpcore<3.7,>=3.6\n -> pulp-python-3.0.0b11                requirement: pulpcore>=3.6\n -> pulp-maven-0.1.0                    requirement: pulpcore>=3.1\n\nCompatible with pulpcore-3.6.1\n -> pulp-certguard-1.0.2                requirement: pulpcore<3.7,>=3.3\n -> pulp-rpm-3.6.2                      requirement: pulpcore<3.7,>=3.6\n -> pulp-cookbook-0.1.0b8               requirement: pulpcore>=3.6.0\n -> pulp-container-2.0.1                requirement: pulpcore<3.7,>=3.6\n -> pulp-file-1.2.0                     requirement: pulpcore<3.7,>=3.6\n -> pulp-ansible-0.3.0                  requirement: pulpcore<3.7,>=3.6\n -> pulp-npm-0.1.0a1.dev0               requirement: pulpcore>=3.0.0rc7\n -> pulp-deb-2.6.1                      requirement: pulpcore<3.7,>=3.6\n -> pulp-python-3.0.0b11                requirement: pulpcore>=3.6\n -> pulp-maven-0.1.0                    requirement: pulpcore>=3.1\n```\n',
    'author': 'Fabricio Aguiar',
    'author_email': 'fabricio.aguiar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
