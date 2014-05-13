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

Usage
=====

PackTeX supports all your standard package manager commands.

* `packtex list` == list all installed packages and their version
* `packtex show` == show info about an installed package, its dependencies, etc.
* `packtex install` == install a package. If a filename (e.g. texrequirements.txt) is passed in, it will install all requirements from that file
* `packtex uninstall` == uninstall a package
* `packtex reinstall` == force a package reinstallation
* `packtex update` == update a package, if it's out of date
* `packtex freeze` == freeze all package details to be exported into a requirements file

And coming soon:
* `packtex search` == search for packages on CTAN
