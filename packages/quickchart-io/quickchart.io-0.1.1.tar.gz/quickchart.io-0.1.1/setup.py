# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickchart-python', 'quickchart-python.examples']

package_data = \
{'': ['*'],
 'quickchart-python': ['.git/*',
                       '.git/hooks/*',
                       '.git/info/*',
                       '.git/logs/*',
                       '.git/logs/refs/heads/*',
                       '.git/logs/refs/remotes/origin/*',
                       '.git/objects/0b/*',
                       '.git/objects/16/*',
                       '.git/objects/1b/*',
                       '.git/objects/1c/*',
                       '.git/objects/36/*',
                       '.git/objects/42/*',
                       '.git/objects/45/*',
                       '.git/objects/59/*',
                       '.git/objects/68/*',
                       '.git/objects/69/*',
                       '.git/objects/8b/*',
                       '.git/objects/98/*',
                       '.git/objects/9b/*',
                       '.git/objects/9e/*',
                       '.git/objects/a6/*',
                       '.git/objects/b3/*',
                       '.git/objects/c0/*',
                       '.git/objects/ed/*',
                       '.git/objects/pack/*',
                       '.git/refs/heads/*',
                       '.git/refs/remotes/origin/*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'quickchart.io',
    'version': '0.1.1',
    'description': 'A client for quickchart.io, a service that generates static chart images',
    'long_description': None,
    'author': 'Ian Webster',
    'author_email': 'ianw_pypi@ianww.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
