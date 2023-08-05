*****************************
This is my first pypi package
*****************************

poetry 
------
- step 1: install poetry using 
    
    .. code-block:: sh
    
        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python    

    before using the above code in Ubuntu system, you must set the default python to the version you want. Because by default python is set to version 2.7 in Ubuntu.

- step 2: Create a new project

    .. code-block:: sh 

        poetry new [project-name]
    
    The output will create a structured project. It will create a 'pyproect.toml' file also . This '.toml' file will have all the configuration for project.

- step 3: Some useful cli commands for poetry 
    
    .. code-block:: sh

        # add packages to project
            poetry add numpy, pandas 
        
        # checking
            poetry check 

        # build the package 
            poetry build 

        # publish to pypi 
            poetry publish 
        
        # venv of poetry 
            poetry shell

Poetry + Vscode
---------------

- step 1: open the project with vscode.

- step 2: Set the environment:

    .. code-block:: sh 

        # add the poetry venv directory path to vscode setting
            "python.venvPath": "~/.cache/pypoetry/virtualenvs"

        # now add the python path from down below bar of vscode 
        # to project env.

- step 3: Set the testing in vscode:

    .. code-block:: sh 

        # open command palette
            'ctrl' + 'shift' + 'p'

        # search for 'test' in command palette
            
        # choose the python test from drop down

        # Then select pytest from drop down 

        # In the down below of vscode a lightning 
        # 'Run test' will appear

        # In the left side of vscode a chemistry 
        # lab flask will appear for testing your tests. 

Poetry + Sphinx
---------------

- step 1: Add the package in development mode 

    .. code-block:: sh 

        poetry add -D sphinx

- step 2: Create a new doc directory and inside it run `sphinx-quickstart`. Then fill out all the things it asks, incase of not knowing just press enter, it will take the default setting.

- step 3: The 'docs' folder now will contain `_build`, `conf.py` and `index.rst`. We need to edit them.

- step 4: Open `conf.py`

    .. code-block:: sh

        # Uncomment them

            import os
            import sys

            sys.path.insert(0, os.path.abspath(".."))

        # Add sphinx packages and theme

            extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

            # html_theme = "alabaster"
              html_theme = "nature"


- step 5: Use `make html` command for building html pages.

- step 6: open the html from `docs/_build/html/index.html`