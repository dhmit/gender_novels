# How to Install the Gutenberg Module

The Gutenberg module requires installation of BSD-DB in addition to the package. Here are the instructions for that, copy-pasted from their readme: 

Linux
*****

On Linux, you can usually install BSD-DB using your distribution's package
manager. For example, on Ubuntu, you can use apt-get:

    sudo apt-get install libdb++-dev
    export BERKELEYDB_DIR=/usr
    pip install -r requirements-py3.pip

MacOS
*****

On Mac, you can install BSD-DB using `homebrew <https://homebrew.sh/>`_:

    brew install berkeley-db4
    pip install -r requirements-py3.pip

Windows
*******

On Windows, it's easiest to download a pre-compiled version of BSD-DB from
`pythonlibs <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_.

For example, if you have Python 3.5 on a 64-bit version of Windows, you
should download :code:`bsddb3‑6.2.1‑cp35‑cp35m‑win_amd64.whl`.

After you download the wheel, install it and you're good to go:

    pip install bsddb3‑6.2.1‑cp35‑cp35m‑win_amd64.whl
 
