# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rug']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'rug',
    'version': '0.2.1',
    'description': 'Library for fetching various stock data from the internet (official and unofficial APIs).',
    'long_description': '# Rug\n\nUniversal library for fetching Stock data from the internet - mostly unofficial\nAPIs - no limits, more free data.\n\n(for Cryptocurrency alternative see [karpet](https://github.com/im-n1/karpet))\n\n* [PyPI](https://pypi.org/project/rug/)\n* [documentation](https://rug.readthedocs.io/en/latest/) ![Documentation Status](https://readthedocs.org/projects/rug/badge/?version=latest)\n\n## Changelog\n\n### 0.2.1\n\nMethod `rug.yahoo.UnofficialAPI.get_current_price()` returns market state now.\n\n### 0.2\n\nNew portals added: YAHOO! + StockTwits\n\n* `get_current_price()` method added\n* `get_earnings_calendar` method added\n\n### 0.1.2\n* `get_dividends()` now returns dividend `amount` too\n\n### 0.1.1\n* dates are now `datetime.date` instance\n\n### 0.1\n* initial release\n',
    'author': 'Pavel Hrdina, Patrick Roach',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/im-n1/rug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
