PackTeX
=======

[![Version](https://badge.fury.io/py/packtex.png)](https://pypi.python.org/pypi/packtex)
[![Downloads](https://pypip.in/d/packtex/badge.png)](https://pypi.python.org/pypi/packtex)
[![Build Status](https://travis-ci.org/TheKevJames/packtex.svg?branch=master)](https://travis-ci.org/TheKevJames/packtex)
[![Coverage Status](https://coveralls.io/repos/TheKevJames/packtex/badge.png?branch=master)](https://coveralls.io/r/TheKevJames/packtex?branch=master)
[![Dependency Status](https://gemnasium.com/TheKevJames/packtex.svg)](https://gemnasium.com/TheKevJames/packtex)

PackTeX is an easy-to-use, platform-agnostic *TeX package manager.

PackTeX lets you manage all of your *TeX packages together, in the same way, without having to worry about using different package managers depending on your system or TeX version.

Installation
============
PackTeX is now available from [PyPI](https://pypi.python.org/pypi/packtex/)! You can instll the latest beta with:

    pip install packtex --pre

Or you can build PackTeX from source by cloning this repo and running:

    python setup.py install

Some Mac OS X users have reported difficulty in installing PackTeX. The solution, it seems, is to tell pip to install `argparse` from non-standard sources. So, call:

    sudo pip install argparse --allow-external argparse --upgrade

and then run either of the installation options again.

Usage
=====

PackTeX supports all your standard package manager commands.

* `packtex list` == list all installed packages and their version
* `packtex show` == show info about an installed package, it's dependencies, etc.
* `packtex install` == install a package
* `packtex uninstall` == uninstall a package
* `packtex update` == update a package, if it's out of date.
* `packtex freeze` == freeze all package details to be exported into a requirements file

And coming soon:
* `packtex search` == search for packages on CTAN
* `packtex install -r` == install all packages from a requirements file
