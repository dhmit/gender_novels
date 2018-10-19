# How to Install the Gutenberg Module

The Gutenberg module requires installation of BSD-DB in addition to the package. Here are the instructions for that, copy-pasted from their readme: 

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

On Mac, you can install BSD-DB using [homebrew](<https://homebrew.sh/>):
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
Remember to install this in your virtual environment, otherwise the thing won't work.  Just 
activate your virtual environment in Powershell, cd to the directory where you saved the thing, 
and then run the command.  Then you can install gutenberg normally.  

Alright, back to me: 

None of the metadata functions will work until you do this: 
```
    from gutenberg.acquire import get_metadata_cache
    cache = get_metadata_cache()
    cache.populate()
```
    
Sadly, depending on the speed of your machine, this could take several hours.  The file isn't that large, it just takes a long time to process.  
Fortunately, you only need to do this once.  If you aren't using any metadata functions, 
you don't need to populate right now and can probably put it off.  (In theory, only the computer generating the metadata csv should need this).
