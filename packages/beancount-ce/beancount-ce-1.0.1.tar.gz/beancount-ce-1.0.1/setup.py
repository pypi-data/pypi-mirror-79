# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_ce']

package_data = \
{'': ['*']}

install_requires = \
['beancount==2.3.0',
 'pdfminer.six>=20200726,<20200727',
 'regex>=2020.7.14,<2021.0.0']

setup_kwargs = {
    'name': 'beancount-ce',
    'version': '1.0.1',
    'description': "Beancount Importer for Caisse d'Epargne PDF statement exports",
    'long_description': "# Beancount Caisse d'Epargne Importer\n\n[![GitHub](https://img.shields.io/github/license/ArthurFDLR/beancount-ce)](https://github.com/ArthurFDLR/beancount-ce/blob/master/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/beancount-ce)](https://pypi.org/project/beancount-ce/)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/beancount-ce)\n\n`beancount-ce` provides a PDF statements importer for the bank [Caisse d'Epargne](http://www.caisse-epargne.fr) to the [Beancount](http://furius.ca/beancount/) format.\n\n## Installation\n\n```console\n    $ pip install beancount-ce\n```\n\n## Usage\n\n```python\n    IBAN_NUMBER_CE = 'FR00 1111 2222 3333 4444 5555 666'\n\n    CONFIG = [\n        CEImporter(\n            iban=IBAN_NUMBER_CE,\n            account='Assets:FR:CdE:CompteCourant',\n            expenseCat='Expenses:FIXME',    #Optional\n            creditCat='Income:FIXME',       #Optional\n            showOperationTypes=False        #Optional\n        ),\n    ]\n```\n",
    'author': 'Arthur Findelair',
    'author_email': 'arthfind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArthurFDLR/beancount-ce',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
