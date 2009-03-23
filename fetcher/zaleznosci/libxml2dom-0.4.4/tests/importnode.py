#!/usr/bin/env python

import libxml2dom
import sys

d = libxml2dom.parse(sys.argv[1])
root = d.xpath("*[1]")[0]
d2 = libxml2dom.createDocument(None, "new", None)
root2 = d2.xpath("*[1]")[0]
for i in range(0, 10):
    imported = d2.importNode(root, 1)
    root2.appendChild(imported)
libxml2dom.toStream(d2, sys.stdout)
#del root2
_d2 = d2.as_native_node()
#del d2
_d2.freeDoc()
#del root
_d = d.as_native_node()
#del d
_d.freeDoc()

# vim: tabstop=4 expandtab shiftwidth=4
