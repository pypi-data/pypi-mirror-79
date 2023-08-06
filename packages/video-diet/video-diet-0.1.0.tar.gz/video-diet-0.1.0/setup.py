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
    'version': '0.1.0',
    'description': '',
    'long_description': '# Video diet\n\nThis project aims to reduce the spaces of your videos enconding it on hevc.\n\n## For developers\n\nYou must first install *poetry*:\n\n```bash\npip install poetry\n```\n\nand inside the project make `poetry install` and after `poetry shell` for start the virtualenv.\nFor testing the code run `video-diet`.\nGood luck 😉.\n\nProject Structure based on awesome tutorial by @tiangolo at https://typer.tiangolo.com/tutorial/package/\n\nhttps://ffmpeg.org/download.html\n',
    'author': 'hian',
    'author_email': 'hiancdtrsnm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
