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
    'version': '0.1.8',
    'description': 'CLI Util for project code gen by jinja snippets',
    'long_description': '<p  align="center">\n<a  href="https://github.com/Egnod/koroviev">\n<img width="500" src="https://gist.githubusercontent.com/Egnod/7cf16c66ed6da1656b069cf89b862aa8/raw/7bc095078d53f7384d5a5b44d47a2195fb76411c/krv_logo.svg">\n</a>\n<h1  align="center">\nKoroviev\n</h1>\nCode jinja template generator for structured projects :)<br>\n<br>\n<img alt="PyPI" src="https://img.shields.io/pypi/v/koroviev?style=for-the-badge">\n</p>\n\n## Install\n```bash\npip3 install koroviev\n```\n\n## Help and init\nFor see commands list (man), type to console:\n```bash\nkoroviev\n```\n\nFor init, type to console (in project root folder):\n```bash\nkoroviev init\n```\n\n## Simple example: Create template and generate\nTest project structure:\n```bash\ntest_project\n├── .koroviev_templates\n├── .koroviev.toml\n└── test_project\n    ├── ... other ...\n    ├── base.py\n    └── cruds\n```\n\nFor example, I add one template with name "crud" in my config file (.koroviev.toml) with two params\n```toml\n[setup]\nlanguage = \'python\'\nproject_folder = \'test_project\'\ntemplates_folder = \'.koroviev_templates\'\ntemplate_extension = \'py\'\n\n[templates.crud]\ncomment = "my test template"\ntarget_project_dir = "cruds/"\nparams = ["name", "table"]\n```\n\nFor easy get auto generate templates folder structure\n```bash\nkoroviev structure generate\n```\n```bash\nCreate template type folder \'unary\': \'/home/user/projects/test_project/.koroviev_templates/unary\'...\nCreate template file \'test\': \'/home/user/projects/test_project/.koroviev_templates/unary/test.py\'...\n```\n\nStructure after template folder generate:\n```bash\ntest_project\n├── .koroviev_templates\n│\xa0\xa0 └── unary\n│\xa0\xa0     └── crud.py\n├── .koroviev.toml\n└── test_project\n    ├── ... other ...\n    ├── base.py\n    └── cruds\n```\n\nFill crud.py with this code:\n```python\nfrom test_project.base import BaseCRUD\n\nclass {{name|capitalize}}CRUD(BaseCRUD):\n    table = "{{table}}"\n```\n\nNext, generate "test" crud by this template:\n```bash\n$ koroviev gen crud\nInput name for generated file: test\nInput \'name\' value: test\nInput \'table\' value: test\nCreate file by template: /home/user/projects/test_project/test_project/cruds/test.py...\n```\n\nResult `cruds/test.py`:\n```python\nfrom test_project.base import BaseCRUD\n\nclass TestCRUD(BaseCRUD):\n    table = "test"\n```\n',
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
