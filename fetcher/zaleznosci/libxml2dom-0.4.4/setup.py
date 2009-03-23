#! /usr/bin/env python

from distutils.core import setup

import libxml2dom

setup(
    name         = "libxml2dom",
    description  = "PyXML-style API for the libxml2 Python bindings",
    author       = "Paul Boddie",
    author_email = "paul@boddie.org.uk",
    url          = "http://www.boddie.org.uk/python/libxml2dom.html",
    version      = libxml2dom.__version__,
    packages     = ["libxml2dom", "libxml2dom.macrolib"],
    scripts      = ["tools/libxml2macro.py"]
    )
