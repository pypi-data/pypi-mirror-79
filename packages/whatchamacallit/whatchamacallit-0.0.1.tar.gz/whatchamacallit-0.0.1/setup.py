# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatchamacallit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'whatchamacallit',
    'version': '0.0.1',
    'description': 'Helper for In Place web servers.',
    'long_description': '# whatchamacallit\n\n# Configure Poetry\n\n````shell script\npoetry publish\n````\n\n\n# Build\n\n````shell script\npoetry build\n````\n\n# Publishing to PyPI\n\n````shell script\npoetry publish\n````\n',
    'author': 'Wolfgang Kühn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decatur/insituwebserver',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
