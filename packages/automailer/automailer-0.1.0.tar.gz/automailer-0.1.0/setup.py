# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automailer']

package_data = \
{'': ['*']}

install_requires = \
['markdown2>=2.3.9,<3.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'yagmail>=0.13.237,<0.14.0']

entry_points = \
{'console_scripts': ['automailer = automailer.__main__']}

setup_kwargs = {
    'name': 'automailer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jacob Clarke',
    'author_email': 'jacobclarke718@gmail.com',
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
