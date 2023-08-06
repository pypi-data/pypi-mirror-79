# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatchamacallit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'whatchamacallit',
    'version': '0.0.2',
    'description': 'Helper for In Place web servers.',
    'long_description': '# whatchamacallit\n\nUse web resources the pythonic way. Specify Javascript modules, HTML, CSS as bare URLs and rewrite on the fly.\n\n# Examples\n\n\n# Configure Poetry\n\n````shell script\npoetry publish\n````\n\n\n# Build\n\n````shell script\npoetry build\n````\n\n# Publishing to PyPI\n\n````shell script\npoetry publish\n````\n\n# Previous Work\n\n\n# Bundlers:\n# Unpkg.com, rollup, webpack, babel, pika, assetgraph, Browserify, gulp, JSPM\n# In Place:\n# snowflake, Open Web Components, browser sync, es-module-shims\n# See\n#   http://dplatz.de/blog/2019/es6-bare-imports.html\n#   https://jakearchibald.com/2017/es-modules-in-browsers/\n#   https://medium.com/@dmnsgn/in-2020-go-bundler-free-eb29c1f05fc9\n#   https://wicg.github.io/import-maps/\n#   https://medium.com/@dmnsgn/es-modules-in-the-browser-almost-now-3638ffafdc68\n',
    'author': 'Wolfgang Kühn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decatur/whatchamacallit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
