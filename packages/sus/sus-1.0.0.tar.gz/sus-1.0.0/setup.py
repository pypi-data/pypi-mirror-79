# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sus = src.sus:sus']}

setup_kwargs = {
    'name': 'sus',
    'version': '1.0.0',
    'description': 'Really simple static website URL shortener',
    'long_description': 'sus: Static URL Shortener\n=========================\n\n**sus** is a static site based URL shortener.\nSimple idea: generate a static site with a bunch of\n``redirect-slug-goes-here/index.html`` files with nothing but an HTML redirect in them.\n\n.. image:: https://github.com/nkantar/sus/workflows/Automated%20Checks/badge.svg\n\n\nInstallation\n------------\n\n.. code-block:: sh\n\n    pip install sus\n\n\nUsage\n-----\n\n#. Install package\n#. Have an ``input`` file ready\n#. Run ``sus`` in the same directory as ``input``\n#. Voil\xc3\xa0\xe2\x80\x94your results are in the ``output/`` directory\n\n\nInput\n-----\n\nsus expects to find a file named ``input`` in the current directory, and each row\nconsists of the redirect slug and destination URL, separated by a pipe (``|``).\n\nE.g.,\n\n.. code-block::\n\n    nk|https://nkantar.com\n    sus|https://github.com/nkantar/sus\n\nIf I were serve the ``output/`` on `<https://sus-example.nkantar.com>`_, then\n`<https://sus-example.nkantar.com/nk>`_ would redirect to `<https://nkantar.com>`_ and\n`<https://sus-example.nkantar.com/sus>`_ would redirect to\n`<https://github.com/nkantar/sus>`_.\n\nNote: That example site exists, and its repository can be found at\n`<https://github.com/nkantar/sus-example.nkantar.com>`_.\n\n\nDevelopment\n-----------\n\nThe project by default uses `Poetry <https://python-poetry.org/>`_, and ``make install``\nshould get you up and running with all the dev dependencies.\nAfter that see other ``make`` commands for convenience.\nThey correspond to CI checks required for changes to be merged in.\n\nThe ``main`` branch is the bleeding edge version.\n`Git tags <https://github.com/nkantar/sus/tags>`_ correspond to releases.\n\n\nContributing Guidelines\n-----------------------\n\nContributions of all sorts are welcome, be they bug reports, patches, or even just\nfeedback.\nCreating a `new issue <https://github.com/nkantar/sus/issues/new>`_ or\n`pull request <https://github.com/nkantar/sus/compare>`_ is probably the best way to get\nstarted.\n\nPlease note that this project is released with a\n`Contributor Code of Conduct <https://github.com/nkantar/sus/blob/master/CODE_OF_CONDUCT.md>`_.\nBy participating in this project you agree to abide by its terms.\n\n\nLicense\n-------\n\nThis project is licensed under the MIT license. See ``LICENSE`` file for details.\n',
    'author': 'Nik Kantar',
    'author_email': 'nik@nkantar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nkantar/sus',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
