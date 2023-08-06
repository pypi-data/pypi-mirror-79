# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['thc_net', 'thc_net.explainable_model', 'thc_net.image']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn==0.23.1', 'tensorflow-addons==0.11.2', 'tensorflow==2.2.0']

setup_kwargs = {
    'name': 'thc-net',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Hartorn',
    'author_email': 'hartorn.github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
