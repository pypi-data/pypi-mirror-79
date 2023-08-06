# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demonstration']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'demonstration',
    'version': '0.2.0',
    'description': 'Demo package for learning Python development',
    'long_description': '# python-package-template\n\n[![PyPI](https://img.shields.io/pypi/v/demonstration.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/demonstration/)\n[![Python](https://img.shields.io/pypi/pyversions/demonstration.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/demonstration/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/python-package-template/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/python-package-template/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nTemplate repository for creating Python packages with GitHub\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/python-package-template/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
