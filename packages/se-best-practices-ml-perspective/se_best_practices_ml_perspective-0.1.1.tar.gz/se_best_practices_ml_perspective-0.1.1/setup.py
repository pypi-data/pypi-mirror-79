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
    'version': '0.1.1',
    'description': 'An opinionated, pedagogical guide on software engineering best practices for those of us in machine learning.',
    'long_description': '![build](https://github.com/JohnGiorgi/se_best_practices_ml_perspective/workflows/build/badge.svg)\n\n# Software Engineering Best Practices, a Machine Learners Perspective\n\nThis repository is meant to serve as an opinionated, pedagogical guide on software engineering best practices for those of us in machine learning.\n\n__What is this guide NOT?__\n\nIt is _NOT_ a comprehensive overview of best practices in software engineering. It is a highly opinionated sampling of tools and ideas that are important for writing good code in a machine learning project. This includes linting, formatting and testing.\n\n__Who is this guide for?__\n\nMachine learners who are not currently following software engineering best practices in their projects but would like to.\n\n__What is machine learning specific about this guide?__\n\nIn truth, nothing important. We use Python as the language of choice as it is popular in machine learning, and we write some machine learning specific tests. Otherwise, this guide could apply to (almost) any python project.\n\n__What tools will this guide cover?__\n\n- [`Poetry`](https://python-poetry.org/docs/#system-requirements), for managing virtual environments and package dependencies.\n- [`flake8`](https://flake8.pycqa.org/en/latest/), for linting.\n- [`black`](https://pypi.org/project/black/), for formatting.\n- [`pytest`](https://docs.pytest.org/en/latest/), for testing.\n- [GitHub Actions](https://github.com/features/actions), for continous integration / continous development (CI/CD).\n\nFollow along with the guide here: https://johngiorgi.github.io/se_best_practices_ml_perspective/.',
    'author': 'johngiorgi',
    'author_email': 'johnmgiorgi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://johngiorgi.github.io/se_best_practices_ml_perspective/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
