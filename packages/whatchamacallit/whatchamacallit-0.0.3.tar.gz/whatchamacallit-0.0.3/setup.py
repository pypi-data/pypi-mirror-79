# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatchamacallit', 'whatchamacallit.examples']

package_data = \
{'': ['*']}

install_requires = \
['importlib-resources>=3.0,<4.0']

setup_kwargs = {
    'name': 'whatchamacallit',
    'version': '0.0.3',
    'description': 'Use web resources the pythonic way, import JavaScript modules like you do with Python modules.',
    'long_description': '# whatchamacallit\n\nUse web resources the pythonic way. Import Javascript modules like you do with Python modules.\nSpecify Javascript modules, HTML, CSS as bare URLs and rewrite on the fly.\n\n# Example\n\n(A) First install the desired package\n````shell script\npip install gridchen\n````\n\n(B) Then from HTML/JavaScript\n````HTML\n<!DOCTYPE html>\n<h1>Hello World</h1>\n<script type="module">\n    import * as utils from "gridchen/utils.js";\n    const tm = utils.createTransactionManager();\n</script>\n````\n\n(C) Configure the import map\n````python\nspec_mapping: Dict[str, str] = {\'gridchen/\': \'/gridchen/\'}\n````\n\n(D) Run one of the example servers (FastAPI or Flask)\n\n# Working\n\nUltimately, the `import * as utils from "gridchen/utils.js"` must be mapped to its physical location, for example\n`/C/projects/myproject/venv/Lib/site-packages/gridchen/utils.js`.\nThis is done in two steps.\n\n## Remap bare import specifier\n\nThe `import * as utils from "gridchen/utils.js"` is **not** valid JavaScript. So at HTML/JavaScript load time the\nimport is remapped to `import * as utils from "/gridchen/utils.js"`\n\n## Route resources to package modules\n\nWhen the server now gets the request for `/gridchen/utils.js`, then it needs to resolve to the package `gridchen`\nand serve its resource `utils.js`.\n\n# Configure Poetry\n\n````shell script\npoetry publish\n````\n\n\n# Build\n\n````shell script\npoetry build\n````\n\n# Publishing to PyPI\n\n````shell script\npoetry publish\n````\n\n# Previous Work\n\n\n# Bundlers:\n# Unpkg.com, rollup, webpack, babel, pika, assetgraph, Browserify, gulp, JSPM\n# In Place:\n# snowflake, Open Web Components, browser sync, es-module-shims\n# See\n#   http://dplatz.de/blog/2019/es6-bare-imports.html\n#   https://jakearchibald.com/2017/es-modules-in-browsers/\n#   https://medium.com/@dmnsgn/in-2020-go-bundler-free-eb29c1f05fc9\n#   https://wicg.github.io/import-maps/\n#   https://medium.com/@dmnsgn/es-modules-in-the-browser-almost-now-3638ffafdc68\n',
    'author': 'Wolfgang Kühn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decatur/whatchamacallit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
