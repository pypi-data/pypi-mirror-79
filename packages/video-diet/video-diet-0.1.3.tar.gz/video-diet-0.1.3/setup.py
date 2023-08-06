# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video_diet']

package_data = \
{'': ['*']}

install_requires = \
['enlighten>=1.6.2,<2.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'ffprobe-python>=1.0.3,<2.0.0',
 'filetype>=1.0.7,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['video-diet = video_diet.main:app']}

setup_kwargs = {
    'name': 'video-diet',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Video diet\n\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?label=license)](https://www.gnu.org/licenses/gpl-3.0) [![Last commit](https://img.shields.io/github/last-commit/hiancdtrsnm/video-diet.svg?style=flat)](https://github.com/hiancdtrsnm/video-diet/commits) [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hiancdtrsnm/video-diet)](https://github.com/hiancdtrsnm/video-diet/commits) [![Github Stars](https://img.shields.io/github/stars/hiancdtrsnm/video-diet?style=flat&logo=github)](https://github.com/hiancdtrsnm/video-diet) [![Github Forks](https://img.shields.io/github/forks/hiancdtrsnm/video-diet?style=flat&logo=github)](https://github.com/hiancdtrsnm/video-diet) [![Github Watchers](https://img.shields.io/github/watchers/hiancdtrsnm/video-diet?style=flat&logo=github)](https://github.com/hiancdtrsnm/video-diet) [![GitHub contributors](https://img.shields.io/github/contributors/hiancdtrsnm/video-diet)](https://github.com/hiancdtrsnm/video-diet/graphs/contributors)\n\nThis project aims to reduce the spaces of your videos encoding it on `hevc`.\n\n## Why video-diet?\nThe answer is easy. I have a lot old-movies/videos taking a lot of space in the hard-drive.\nSo I\'m always short on disk space, the by accident discover de `hevc` codec. when i need to shrink a video of `3GB`\nto upload it to `Telegram`, the convertion take my 3GB movie and returned a 300 MB with the same quality 😱. So I\ndecided that I would convert all my video files, but they are a lot, so I build this tool for it.\n\nMore info about `hevc`:\n\nhttps://en.wikipedia.org/wiki/High_Efficiency_Video_Coding\n\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install video-diet\n```\n\n</div>\n\n## FFMPEG\n\nIn order to run the project you must install `ffmpeg`.\n\n### For Linux\nIn any linux machine you can get it from your favorite package manager.\n\nFor arch:\n```console\nsudo pacman -S ffmpeg\n```\n\nFor Debian/Ubuntu:\n```console\nsudo apt-get install ffmpeg\n```\n\n## For Windows\n\nhttps://ffmpeg.org/download.html\n\n\n## Example\n\n### For a file\n\n```bash\nvideo-diet file test.mp4\n```\nThis option conserve the original file\n\n## For a folder\n```bash\nvideo-diet folder ~/Videos\n```\nThis option replaces the original file for the converted files\n\n## Note\n\nThe video conversion can take some time. Depending on the original video properties; the conversion time can be longer than the video.\n\n## For developers\n\n### You must first install *poetry*\n\nPoetry provides a custom installer that will install `poetry` isolated from the rest of your system by vendorizing its dependencies. This is the recommended way of installing `poetry`.\n\n**osx / linux / bashonwindows install instructions**\n\n`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`\n\n**windows powershell install instructions**\n\n`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python`\n\nThe installer installs the `poetry` tool to Poetry\'s `bin` directory. On Unix it is located at `$HOME/.poetry/bin` and on Windows at `%USERPROFILE%\\.poetry\\bin`.\n\nThis directory will be in your `$PATH` environment variable, which means you can run them from the shell without further configuration.\n\n### Then you need to configure the environment\n\nInside the project make `poetry install` and after `poetry shell` for start the virtualenv.\n\nFor testing the code run `video-diet`.\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md) for more details.\n\nGood luck 😉.\n\nProject Structure based on awesome tutorial by @tiangolo at https://typer.tiangolo.com/tutorial/package\n',
    'author': 'hian',
    'author_email': 'hiancdtrsnm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
