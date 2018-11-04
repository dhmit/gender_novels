# How to Install the Gutenberg Module

## Do I need to Install the Gutenberg Module?

If you're only interested in using the already compiled books and metadata, and not 
`corpus_gen.py`, installing gutenberg or bsddb isn't necessary.  You'll just see a message 
`Cannot import gutenberg`.  

## Installation Instructions

The Gutenberg module requires installation of BSD-DB in addition to the package. Here are the 
instructions for that, copy-pasted from [their readme](https://github.com/c-w/gutenberg/blob/master/README.rst): 

Linux
*****

On Linux, you can usually install BSD-DB using your distribution's package
manager. For example, on Ubuntu, you can use apt-get:

```
    sudo apt-get install libdb++-dev
    export BERKELEYDB_DIR=/usr
    pip install -r requirements-py3.pip
```

MacOS
*****

On Mac, you can install BSD-DB using [homebrew](<https://brew.sh/>):

```
    brew install berkeley-db4
    pip install -r requirements-py3.pip
```

Windows
*******

On Windows, it's easiest to download a pre-compiled version of BSD-DB from
[pythonlibs](<http://www.lfd.uci.edu/~gohlke/pythonlibs/>).

For example, if you have Python 3.5 on a 64-bit version of Windows, you
should download `bsddb3‑6.2.1‑cp35‑cp35m‑win_amd64.whl`.

After you download the wheel, install it and you're good to go:

```
    pip install bsddb3‑6.2.1‑cp35‑cp35m‑win_amd64.whl
```

If you're using a virtual environment, be sure to activate your environment first.


After installing BSD-DB, gutenberg can be installed normally.  

None of the metadata functions will work until you do this: 

```python

    from gutenberg.acquire import get_metadata_cache
    
    cache = get_metadata_cache()
    
    cache.populate()
```
    
Depending on the speed of your machine, this could take several hours.  Fortunately, the file isn't 
that large, it just takes a long time to process.  

## IOError

If after interrupting the corpus generation and trying to run it again you encounter `IOError: 
[Errno 9] Bad file descriptor`, try running the 
[db_recover](http://pybsddb.sourceforge.net/ref/transapp/recovery.html) utility.  
