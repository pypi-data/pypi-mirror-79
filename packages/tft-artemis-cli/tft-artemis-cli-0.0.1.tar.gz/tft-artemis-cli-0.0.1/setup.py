# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tft', 'tft.artemis_cli']

package_data = \
{'': ['*'], 'tft.artemis_cli': ['schemas/*']}

install_requires = \
['click',
 'click_completion>=0.5.2,<0.6.0',
 'click_spinner',
 'jsonschema',
 'requests',
 'rich>=2.2.6,<3.0.0',
 'ruamel.yaml>=0.15.51,<0.16.0',
 'stackprinter>=0.2.4,<0.3.0',
 'tabulate',
 'urlnormalizer>=1.2.5,<2.0.0']

entry_points = \
{'console_scripts': ['artemis-cli = tft.artemis_cli.artemis_cli:cli_root']}

setup_kwargs = {
    'name': 'tft-artemis-cli',
    'version': '0.0.1',
    'description': 'Comand line tool for Artemis service',
    'long_description': None,
    'author': 'Milos Prchlik',
    'author_email': 'mprchlik@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
