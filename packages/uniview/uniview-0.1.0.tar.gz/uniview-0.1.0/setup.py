# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uniview', 'uniview.IM2D']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0', 'absl-py>=0.10.0,<0.11.0', 'opencv-python==4.2.0.34']

entry_points = \
{'console_scripts': ['run = uniview:main']}

setup_kwargs = {
    'name': 'uniview',
    'version': '0.1.0',
    'description': 'Datapoint Visualization and Illustration Toolkit',
    'long_description': '',
    'author': 'H-AI',
    'author_email': 'dongjian413@gmail.com',
    'maintainer': 'H-AI',
    'maintainer_email': 'dongjian413@gmail.com',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
