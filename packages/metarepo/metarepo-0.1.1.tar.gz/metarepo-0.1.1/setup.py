# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metarepo', 'metarepo.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'gitpython>=3.1.0,<4.0.0',
 'prompt-toolkit>=3.0.7,<4.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['git-meta = metarepo.cli:cli',
                     'metarepo = metarepo.cli:cli']}

setup_kwargs = {
    'name': 'metarepo',
    'version': '0.1.1',
    'description': 'Git Meta Repository Manager',
    'long_description': '# Metarepo: An alternative to git submodules\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/blejdfist/git-metarepo/Python%20package)\n![PyPI - License](https://img.shields.io/pypi/l/metarepo)\n![PyPI](https://img.shields.io/pypi/v/metarepo)\n\nMetarepo is used to manage dependencies on other git repositories when git submodules is not sufficient.\nIt was inspired by the [repo](https://gerrit.googlesource.com/git-repo/) tool by Google but instead of requiring the\nmanifest to be stored in its own repository, it is stored in the same repository.\n\n![Demo](assets/demo.gif)\n\n## Installation\n\n```bash\n# Install from PyPI\npip3 install --upgrade metarepo\n\n# Install from git using PIP\npip3 install --upgrade git+https://github.com/blejdfist/git-metarepo\n```\n\n## Usage\n\nYou can run `metarepo` in two ways, standalone or using git. Both methods work the same and it is only a matter of personal taste.\n\n```bash\ngit meta\nmetarepo\n```\n\nCreate an initial `manifest.yml` configuration using the init command\n```bash\ngit meta init\n```\n\nSynchronize the repositories\n```bash\ngit meta sync\n```\n\n## Manifest structure\n\n```yml\nrepos:\n  - url: https://github.com/blejdfist/pycodegen\n    path: tools/pycodegen\n    track: master\n```\n\n| Field     | Explanation              | Required             |\n| --------- | ------------------------ | :------------------: |\n| url       | Git URL to clone         | Yes                  |\n| path      | Where to clone the repo  | Yes                  |\n| track     | What branch/tag to track | No (default: master) |\n',
    'author': 'Jim Ekman',
    'author_email': 'jim@nurd.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
