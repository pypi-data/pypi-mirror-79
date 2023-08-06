# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyairnow']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'pyairnow',
    'version': '1.0.1',
    'description': 'A lightweight Python wrapper for EPA AirNow Air Quality API',
    'long_description': "# pyairnow: a thin Python wrapper for the AirNow API\n\n[![CI](https://github.com/asymworks/pyairnow/workflows/CI/badge.svg)](https://github.com/asymworks/pyairnow/actions)\n[![PyPi](https://img.shields.io/pypi/v/pyairnow.svg)](https://pypi.python.org/pypi/pyairnow)\n[![Version](https://img.shields.io/pypi/pyversions/pyairnow.svg)](https://pypi.python.org/pypi/pyairnow)\n[![License](https://img.shields.io/pypi/l/pyairnow.svg)](https://github.com/asymworks/pyairnow/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/asymworks/pyairnow/branch/master/graph/badge.svg)](https://codecov.io/gh/asymworks/pyairnow)\n\n`pyairnow` is a simple, tested, thin client library for interacting with the\n[AirNow](https://www.airnow.gov) United States EPA Air Quality Index API.\n\n- [Python Versions](#python-versions)\n- [Installation](#installation)\n- [API Key](#api-key)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n# Python Versions\n\n`pyairnow` is currently supported and tested on:\n\n* Python 3.6\n* Python 3.7\n* Python 3.8\n\n# Installation\n\n```python\npip install pyairnow\n```\n\n# API Key\n\nYou can get an AirNow API key from\n[the AirNow API site](https://docs.airnowapi.org/account/request/). Ensure you\nread and understand the expectations and limitations of API usage, which can\nbe found at [the AirNow FAQ](https://docs.airnowapi.org/faq).\n\n# Usage\n\n```python\nimport asyncio\nimport datetime\n\nfrom pyairnow import WebServiceAPI\n\n\nasync def main() -> None:\n  client = WebServiceAPI('your-api-key')\n\n  # Get current observational data based on a zip code\n  data = await client.observations.zipCode(\n    '90001',\n    # if there are no observation stations in this zip code, optionally\n    # provide a radius to search (in miles)\n    distance=50,\n  )\n\n  # Get current observational data based on a latitude and longitude\n  data = await client.observations.latLong(\n    34.053718, -118.244842,\n    # if there are no observation stations at this location, optionally\n    # provide a radius to search (in miles)\n    distance=50,\n  )\n\n  # Get forecast data based on a zip code\n  data = await client.forecast.zipCode(\n    '90001',\n    # to get a forecast for a certain day, provide a date in yyyy-mm-dd,\n    # if not specified the current day will be used\n    date='2020-09-01',\n    # if there are no observation stations in this zip code, optionally\n    # provide a radius to search (in miles)\n    distance=50,\n  )\n\n  # Get forecast data based on a latitude and longitude\n  data = await client.forecast.latLong(\n    # Lat/Long may be strings or floats\n    '34.053718', '-118.244842',\n    # forecast dates may also be datetime.date or datetime.datetime objects\n    date=datetime.date(2020, 9, 1),\n    # if there are no observation stations in this zip code, optionally\n    # provide a radius to search (in miles)\n    distance=50,\n  )\n\n\nasyncio.run(main())\n```\n\nBy default, the library creates a new connection to AirNow with each coroutine.\nIf you are calling a large number of coroutines (or merely want to squeeze out\nevery second of runtime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used\nfor connection pooling:\n\n```python\nimport asyncio\nimport datetime\n\nfrom aiohttp import ClientSession\n\nfrom pyairnow import WebServiceAPI\n\n\nasync def main() -> None:\n    async with ClientSession() as session:\n        client = WebServiceAPI('your-api-key', session=session)\n\n        # ...\n\n\nasyncio.run(main())\n```\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/asymworks/pyairnow/issues)\n  or [start a discussion on one](https://github.com/asymworks/pyairnow/issues/new).\n2. [Fork the repository](https://github.com/asymworks/pyairnow/fork).\n3. Install [Poetry](https://python-poetry.org/) and set up the development workspace:\n  `poetry install`\n4. Code your new feature or bug fix.\n5. Write tests that cover your new functionality.\n6. Run tests and ensure 100% code coverage: `make test`\n7. Run the linter to ensure 100% code style correctness: `make lint`\n8. Update `README.md` with any new documentation.\n9. Add yourself to `AUTHORS.md`.\n10. Submit a pull request!\n",
    'author': 'Jonathan Krauss',
    'author_email': 'jkrauss@asymworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asymworks/pyairnow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
