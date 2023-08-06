# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plot_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'matplotlib>=3.2.0,<4.0.0', 'pandas>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['plot = plot_cli.core:cli']}

setup_kwargs = {
    'name': 'plot-cli',
    'version': '0.2.0',
    'description': 'Command Line Interface for Data Visualization',
    'long_description': '# Plot CLI\n\nPlot CLI is command line interface for data visualization.\n\n[![PyPi][pypi-version]][pypi] [![Python Version][python-version]][pypi] [![GitHub Workflow Status][actions-status]][actions] [![Documentation][docs-status]][docs] [![codecov][codecov-status]][codecov] [![License][license]][license-file]\n\nIt works on Python 3.6.1 and greater.\n\n## Installation\n\nInstall using pip:\n\n```sh\npip install plot-cli\n```\n\n## Getting Started\n\nYou can output a graph from stdin or a file.\n\n```sh\ncat data.csv | plot line --header --index-col year\n```\n\n![example](https://user-images.githubusercontent.com/6437204/78489195-f0586480-7782-11ea-9160-0cbee89ccaf1.png)\n\nSee the [documentation](https://plot-cli.readthedocs.io/) for detailed usage and examples.\n\n## Change Log\n\nSee [Change Log](CHANGELOG.rst).\n\n[pypi]: https://pypi.org/project/plot-cli\n[pypi-version]: https://img.shields.io/pypi/v/plot-cli\n[python-version]: https://img.shields.io/pypi/pyversions/plot-cli\n[actions]: https://github.com/xkumiyu/plot-cli/actions\n[actions-status]: https://img.shields.io/github/workflow/status/xkumiyu/plot-cli/Python%20package\n[docs]: https://plot-cli.readthedocs.io/\n[docs-status]: https://img.shields.io/readthedocs/plot-cli/latest\n[codecov]: https://codecov.io/gh/xkumiyu/plot-cli\n[codecov-status]: https://img.shields.io/codecov/c/github/xkumiyu/plot-cli\n[license]: https://img.shields.io/github/license/xkumiyu/plot-cli\n[license-file]: https://github.com/xkumiyu/plot-cli/blob/master/LICENSE\n',
    'author': 'xkumiyu',
    'author_email': 'xkumiyu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xkumiyu/plot-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
