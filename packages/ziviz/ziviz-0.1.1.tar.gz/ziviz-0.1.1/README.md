
Ziviz

Exploratory data analysis tool for Jupyter.

Installation
------------

To install use pip:

    $ pip install ziviz
    $ jupyter nbextension enable --py --sys-prefix ziviz

To install for jupyterlab

    $ jupyter labextension install ziviz

For a development installation (requires npm),

    $ git clone https://github.com/ziviz/ziviz.git
    $ cd ziviz
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ziviz
    $ jupyter nbextension enable --py --sys-prefix ziviz
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

