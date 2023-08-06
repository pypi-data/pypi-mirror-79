# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['se_best_practices_ml_perspective']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning>=0.9.0,<0.10.0', 'torchvision>=0.7.0,<0.8.0']

extras_require = \
{'documentation': ['mkdocs-material>=5.5.8,<6.0.0']}

setup_kwargs = {
    'name': 'se-best-practices-ml-perspective',
    'version': '0.1.0',
    'description': 'An opinionated, pedagogical guide on software engineering best practices for those of us in machine learning.',
    'long_description': None,
    'author': 'johngiorgi',
    'author_email': 'johnmgiorgi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
