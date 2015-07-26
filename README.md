PackTeX
=======

[![Version](https://img.shields.io/pypi/v/packtex.svg)](https://pypi.python.org/pypi/packtex)
[![Downloads](https://img.shields.io/pypi/dm/packtex.svg)](https://pypi.python.org/pypi/packtex)
[![Code Quality](https://img.shields.io/codacy/f99d041848054bf18b909cee1bcf866c.svg)](https://www.codacy.com/app/KevinJames/packtex)
[![Build Status](https://img.shields.io/circleci/project/TheKevJames/packtex.svg)](https://circleci.com/gh/TheKevJames/packtex)
[![Requirements](https://img.shields.io/requires/github/TheKevJames/packtex.svg)](https://requires.io/github/TheKevJames/packtex/requirements)

PackTeX is an easy-to-use, platform-agnostic *TeX package manager.

PackTeX lets you manage all of your *TeX packages together, in the same way, without having to worry about using different package managers depending on your system or TeX version.

Installation
============
PackTeX is now available from [PyPI](https://pypi.python.org/pypi/packtex/)! You can install the latest beta with:

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
