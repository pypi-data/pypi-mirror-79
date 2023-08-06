# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mysql2s3']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'minio>=6.0.0,<7.0.0',
 'psutil>=5.7.2,<6.0.0',
 'watchdog>=0.10.3,<0.11.0']

entry_points = \
{'console_scripts': ['mysql2s3 = mysql2s3.mysql2s3:main',
                     'verify-dump = mysql2s3.verify_dump:main']}

setup_kwargs = {
    'name': 'mysql2s3',
    'version': '0.1.0',
    'description': 'Upload Mydumper directories to S3.',
    'long_description': None,
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
