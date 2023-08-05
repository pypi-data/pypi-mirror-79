# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dina_test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'sphinx>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'dina-test',
    'version': '0.1.2',
    'description': '',
    'long_description': '*****************************\nThis is my first pypi package\n*****************************\n\npoetry \n------\n- step 1: install poetry using \n    \n    .. code-block:: sh\n    \n        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python    \n\n    before using the above code in Ubuntu system, you must set the default python to the version you want. Because by default python is set to version 2.7 in Ubuntu.\n\n- step 2: Create a new project\n\n    .. code-block:: sh \n\n        poetry new [project-name]\n    \n    The output will create a structured project. It will create a \'pyproect.toml\' file also . This \'.toml\' file will have all the configuration for project.\n\n- step 3: Some useful cli commands for poetry \n    \n    .. code-block:: sh\n\n        # add packages to project\n            poetry add numpy, pandas \n        \n        # checking\n            poetry check \n\n        # build the package \n            poetry build \n\n        # publish to pypi \n            poetry publish \n        \n        # venv of poetry \n            poetry shell\n\nPoetry + Vscode\n---------------\n\n- step 1: open the project with vscode.\n\n- step 2: Set the environment:\n\n    .. code-block:: sh \n\n        # add the poetry venv directory path to vscode setting\n            "python.venvPath": "~/.cache/pypoetry/virtualenvs"\n\n        # now add the python path from down below bar of vscode \n        # to project env.\n\n- step 3: Set the testing in vscode:\n\n    .. code-block:: sh \n\n        # open command palette\n            \'ctrl\' + \'shift\' + \'p\'\n\n        # search for \'test\' in command palette\n            \n        # choose the python test from drop down\n\n        # Then select pytest from drop down \n\n        # In the down below of vscode a lightning \n        # \'Run test\' will appear\n\n        # In the left side of vscode a chemistry \n        # lab flask will appear for testing your tests. \n\nPoetry + Sphinx\n---------------\n\n- step 1: Add the package in development mode \n\n    .. code-block:: sh \n\n        poetry add -D sphinx\n\n- step 2: Create a new doc directory and inside it run `sphinx-quickstart`. Then fill out all the things it asks, incase of not knowing just press enter, it will take the default setting.\n\n- step 3: The \'docs\' folder now will contain `_build`, `conf.py` and `index.rst`. We need to edit them.\n\n- step 4: Open `conf.py`\n\n    .. code-block:: sh\n\n        # Uncomment them\n\n            import os\n            import sys\n\n            sys.path.insert(0, os.path.abspath(".."))\n\n        # Add sphinx packages and theme\n\n            extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]\n\n            # html_theme = "alabaster"\n              html_theme = "nature"\n\n\n- step 5: Use `make html` command for building html pages.\n\n- step 6: open the html from `docs/_build/html/index.html`',
    'author': 'dinabandhu50',
    'author_email': 'beheradinabandhu50@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
