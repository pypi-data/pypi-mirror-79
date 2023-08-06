# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automailer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'markdown2>=2.3.9,<3.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'yagmail>=0.13.237,<0.14.0']

entry_points = \
{'console_scripts': ['automailer = automailer.client:mail']}

setup_kwargs = {
    'name': 'automailer',
    'version': '0.1.3',
    'description': 'A command line utility for sending customized mass emails.',
    'long_description': '# An Automated Email Sender\n\n``` bash\npip install automailer\n```\n\n## Usage\n\n### file structure\nCreate the following file structure.\n\n```\n/\n    /data\n       email_list.csv\n       message.md \n```\n\n### message.md\n\n``` markdown\n\n---\nsubject: Required Subject for Email\nsender: Required Gmail sender\npassword: OTP for gmail sender\n---\n\nHi {name},\n\nThe cool thing about this file is that you can add any column included in your csv and it will populate. \nYour favorite color is {favorite_color}.\n\nBest,\n\nSender\n```\n\n### email_list.csv\nThe only required column for this file is `email`.\n\n``` csv\nname, favorite_color, email\nJacob, Green, jacob@gmail.com\n```\n\n### Run\n\nChange to root of project. \n\n``` bash\npython -m automailer\n```',
    'author': 'Jacob Clarke',
    'author_email': 'jacobclarke718@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j718/automailer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
