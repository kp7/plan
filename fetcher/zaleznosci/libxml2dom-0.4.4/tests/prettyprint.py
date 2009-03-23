#!/usr/bin/env python

import libxml2dom
from xml.dom.ext import PrettyPrint
import sys

d = libxml2dom.parse(sys.argv[1])
PrettyPrint(d)

# vim: tabstop=4 expandtab shiftwidth=4
