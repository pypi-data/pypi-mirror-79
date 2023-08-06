# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web_command']

package_data = \
{'': ['*'], 'web_command': ['static/*']}

install_requires = \
['aiohttp>=3.0,<4.0', 'ansicolors>=1.0,<2.0', 'ptyprocess>=0.6,<0.7']

entry_points = \
{'console_scripts': ['web-command = web_command.console:main']}

setup_kwargs = {
    'name': 'web-command',
    'version': '0.1.0',
    'description': 'Output a command to a web browser.',
    'long_description': '# Web Command\n\nOutput a command to a web browser console.\n\n## Install\n\n```\npip install web-command\n```\n\n## Example\n\n```sh\nweb-command -s -l info -w 60 -- curl -s https://wttr.in/los-angeles\n```\n\nBrowse http://localhost:8000/ to see the output.\n\n## Usage\n\n```\nusage: web-command [-h] [-a HOST] [-p PORT] [-s] [-l LEVEL] [-w WAIT_TIME]\n                   [-V]\n                   [COMMAND [COMMAND ...]]\n\nOutput a command to a web browser.\n\npositional arguments:\n  COMMAND               command to run (default: None)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -a HOST, --host HOST  host to bind to (default: localhost)\n  -p PORT, --port PORT  port to bind to (default: 8000)\n  -s, --suppress-output\n                        suppress output (default: False)\n  -l LEVEL, --log-level LEVEL\n                        log level (default: none)\n  -w WAIT_TIME, --wait-time WAIT_TIME\n                        seconds to wait before restarting command (default: 5)\n  -V, --version         show version and exit (default: False)\n```\n\n## Development\n\n```sh\ngit clone https://github.com/vjagaro/web-command.git\ncd web-command-server\npoetry install\nnpm install\nnpm run build\n```\n\nTo build and publish:\n\n```sh\npoetry build\npoetry config repositories.testpypi https://test.pypi.org/legacy/\npoetry publish -r testpypi\n# In another virtual environment:\npip install --index-url https://test.pypi.org/simple/ web-command\n# If this looks good...\npoetry publish\n```\n',
    'author': 'Jāgaro',
    'author_email': 'v.jagaro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vjagaro/web-command',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
