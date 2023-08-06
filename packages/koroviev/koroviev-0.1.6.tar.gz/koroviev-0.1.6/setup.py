# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koroviev', 'koroviev.components']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0',
 'jinja2>=2.11.2,<3.0.0',
 'loguru>=0.5.2,<0.6.0',
 'pydantic>=1.6.1,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['koroviev = koroviev.cli:start_cli']}

setup_kwargs = {
    'name': 'koroviev',
    'version': '0.1.6',
    'description': 'CLI Util for project code gen by jinja snippets',
    'long_description': None,
    'author': 'Alexander Lavrov',
    'author_email': 'internal@egnod.dev',
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
