# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funpymodeling', 'funpymodeling.test']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.2,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'sklearn>=0.0,<0.1']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'funpymodeling',
    'version': '0.1.7',
    'description': 'A package designed for data scientists and teachers, to speed up their ML projects, focused on exploratory data analysis, data preparation, and model performance.',
    'long_description': '# funPyModeling\nA package to help data scientist in Exploratory Data Analysis and Data Preparation for ML models\n',
    'author': 'Pablo Casas',
    'author_email': 'pcasas.biz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pablo14/funPyModeling',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
