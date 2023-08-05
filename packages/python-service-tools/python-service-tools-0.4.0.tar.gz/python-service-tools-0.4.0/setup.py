# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['servicetools']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=0.1,<0.2', 'starlette>=0.13,<0.14', 'structlog>=19,<20']

setup_kwargs = {
    'name': 'python-service-tools',
    'version': '0.4.0',
    'description': 'Utilities for working with python services.',
    'long_description': '# python-service-tools\n\nUtilities for working with python services.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/misc-utils-py) ![PyPI](https://img.shields.io/pypi/v/misc-utils-py.svg)\n\n## Usage\n\n### logging_config\n\nDefault configuration for structlog. \n\nConfigure json logging at the INFO level:\n```python\nfrom miscutils.logging_config import default_logging, LogFormat, Verbosity\n\ndefault_logging(Verbosity.INFO, LogFormat.JSON)\n```\n\nConfigure text logging at the DEBUG level:\n```python\nfrom miscutils.logging_config import default_logging, LogFormat, Verbosity\n\ndefault_logging(Verbosity.DEBUG, LogFormat.TEXT)\n```\n\nConfigure text logging at the DEBUG level and filter out external loggers:\n```python\nfrom miscutils.logging_config import default_logging, LogFormat, Verbosity\n\ndefault_logging(Verbosity.DEBUG, LogFormat.TEXT, ["extern_logger_1"])\n```\n\n### Log timing information for a function\n\nDecorator to add timing information to the logs:\n```python\nfrom miscutils.timer import timer\n\nimport structlog\n\n@timer(structlog.get_logger(__name__))\ndef some_function():\n    pass\n```\n\n### Create a namespace relative patch\n\nCreate namespace relative patches:\n```python\nimport some_package.sub_package.another_package as under_test\nfrom miscutils.testing import relative_patch_maker\n\npatch = relative_patch_maker(under_test.__name__)\n\nclass TestStuff:\n    #equivalent to @unittest.mock.patch("some_package.sub_package.another_package.something_to_patch")\n    @patch("something_to_patch")\n    def test_something(self, patched):\n        under_test.something()\n        patched.assert_called_once()\n\n    #equivalent to @unittest.mock.patch("some_package.sub_package.another_package.something_else_to_patch")\n    @patch("something_else_to_patch")\n    def test_something(self, patched):\n        under_test.something()\n        patched.assert_called_once()\n```\n\n### Starlette Structlog middleware \n\nMiddleware for [Starlette](https://www.starlette.io/) framework to log HTTP \nrequests to structlog. Log entries will be made at the start and end of\neach request. Error requests (400s and 500s) will also be logged. Any \ncalls that throw exceptions will be converted 500 responses.\n\n```python\nfrom miscutils.middleware import StructlogRequestMiddleware\nimport structlog\n\napp.add_middleware(StructlogRequestMiddleware(app, logger=structlog.get_logger(__name__)))\n```\n\nThere are options to customize the logging:\n\n```python\nimport logging\n\nimport structlog\nfrom miscutils.middleware import StructlogRequestMiddleware\n\napp.add_middleware(StructlogRequestMiddleware(\n    app,\n    logger=structlog.get_logger(__name__),\n    log_level=logging.DEBUG,  # Log at the DEBUG level.\n    ignored_status_codes={404},  # Do not log 404 errors.\n))\n```\n\n## Development Guide\n\nThis project uses [poetry](https://python-poetry.org/):\n\n```\n$ pip install poetry\n$ cd to/project/root\n$ poetry install\n```\n\n### Testing\n\nTesting is done via pytest.\n\n```\n$ poetry run pytest\n```',
    'author': 'Alexander Costas',
    'author_email': 'alexander.costas@mongodb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mongodb-labs/python-service-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
