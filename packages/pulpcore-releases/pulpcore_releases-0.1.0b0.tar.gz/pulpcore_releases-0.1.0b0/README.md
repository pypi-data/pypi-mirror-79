Pulpcore - Releases & Compatibility
-----------------------------------

List the latest 3 pulpcore releases and its compatible plugins:

```
~ via 🐍 v3.8.0 (venv)
❯ pip install pulpcore-releases
Collecting pulpcore-releases
  Downloading pulpcore_releases-0.1.0-py3-none-any.whl (2.7 kB)
Requirement already satisfied: aiohttp<4.0.0,>=3.6.2 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from pulpcore-releases) (3.6.2)
Requirement already satisfied: packaging<21.0,>=20.4 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from pulpcore-releases) (20.4)
Requirement already satisfied: async-timeout<4.0,>=3.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (3.0.1)
Requirement already satisfied: multidict<5.0,>=4.5 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (4.7.6)
Requirement already satisfied: chardet<4.0,>=2.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (3.0.4)
Requirement already satisfied: yarl<2.0,>=1.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (1.5.1)
Requirement already satisfied: attrs>=17.3.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (20.1.0)
Requirement already satisfied: six in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from packaging<21.0,>=20.4->pulpcore-releases) (1.15.0)
Requirement already satisfied: pyparsing>=2.0.2 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from packaging<21.0,>=20.4->pulpcore-releases) (2.4.7)
Requirement already satisfied: idna>=2.0 in ./.pyenv/versions/3.8.0/envs/venv/lib/python3.8/site-packages (from yarl<2.0,>=1.0->aiohttp<4.0.0,>=3.6.2->pulpcore-releases) (2.10)
Installing collected packages: pulpcore-releases
Successfully installed pulpcore-releases-0.1.0
~ via 🐍 v3.8.0 (venv) took 2s
❯ prc

Compatible with pulpcore-3.6.3
 -> pulp-certguard-1.0.2                requirement: pulpcore<3.7,>=3.3
 -> pulp-rpm-3.6.2                      requirement: pulpcore<3.7,>=3.6
 -> pulp-cookbook-0.1.0b8               requirement: pulpcore>=3.6.0
 -> pulp-container-2.0.1                requirement: pulpcore<3.7,>=3.6
 -> pulp-file-1.2.0                     requirement: pulpcore<3.7,>=3.6
 -> pulp-ansible-0.3.0                  requirement: pulpcore<3.7,>=3.6
 -> pulp-npm-0.1.0a1.dev0               requirement: pulpcore>=3.0.0rc7
 -> pulp-deb-2.6.1                      requirement: pulpcore<3.7,>=3.6
 -> pulp-python-3.0.0b11                requirement: pulpcore>=3.6
 -> pulp-maven-0.1.0                    requirement: pulpcore>=3.1

Compatible with pulpcore-3.6.2
 -> pulp-certguard-1.0.2                requirement: pulpcore<3.7,>=3.3
 -> pulp-rpm-3.6.2                      requirement: pulpcore<3.7,>=3.6
 -> pulp-cookbook-0.1.0b8               requirement: pulpcore>=3.6.0
 -> pulp-container-2.0.1                requirement: pulpcore<3.7,>=3.6
 -> pulp-file-1.2.0                     requirement: pulpcore<3.7,>=3.6
 -> pulp-ansible-0.3.0                  requirement: pulpcore<3.7,>=3.6
 -> pulp-npm-0.1.0a1.dev0               requirement: pulpcore>=3.0.0rc7
 -> pulp-deb-2.6.1                      requirement: pulpcore<3.7,>=3.6
 -> pulp-python-3.0.0b11                requirement: pulpcore>=3.6
 -> pulp-maven-0.1.0                    requirement: pulpcore>=3.1

Compatible with pulpcore-3.6.1
 -> pulp-certguard-1.0.2                requirement: pulpcore<3.7,>=3.3
 -> pulp-rpm-3.6.2                      requirement: pulpcore<3.7,>=3.6
 -> pulp-cookbook-0.1.0b8               requirement: pulpcore>=3.6.0
 -> pulp-container-2.0.1                requirement: pulpcore<3.7,>=3.6
 -> pulp-file-1.2.0                     requirement: pulpcore<3.7,>=3.6
 -> pulp-ansible-0.3.0                  requirement: pulpcore<3.7,>=3.6
 -> pulp-npm-0.1.0a1.dev0               requirement: pulpcore>=3.0.0rc7
 -> pulp-deb-2.6.1                      requirement: pulpcore<3.7,>=3.6
 -> pulp-python-3.0.0b11                requirement: pulpcore>=3.6
 -> pulp-maven-0.1.0                    requirement: pulpcore>=3.1
```
