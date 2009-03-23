#!/usr/bin/env python

import libxml2dom, xml.dom.minidom

def test(document, e):
    e.setAttributeNS("xxx", "yyy", "zzz")
    e.setAttributeNS("xxx", "yyy", "zzz")
    e.setAttributeNS("xxx", "x:yyy", "zzz")
    e.setAttributeNS("xxx", "x:yyy", "zzz")
    e2 = document.createElementNS("DAV:", "d:abc")
    e.appendChild(e2)
    e2.setAttributeNS(None, "pqr", "xyz")
    e2.setAttributeNS("DAV:", "qrs", "tuv")
    e3 = document.createElementNS(None, "def")
    e2.appendChild(e3)
    e3.setAttributeNS("DAV:", "fgh", "ijk")
    e3.setAttributeNS(None, "nop", "wxy")

document = libxml2dom.createDocument(None, "doc", None)
e = document.xpath("*")[0]
test(document, e)
print document.toString(prettyprint=1)

document = xml.dom.minidom.getDOMImplementation().createDocument(None, "doc", None)
e = document.documentElement
test(document, e)
print document.toprettyxml()

try:
    from xml.dom.ext import PrettyPrint
    PrettyPrint(document)
except ImportError:
    print "PrettyPrint not tested."

try:
    import pxdom
    document = pxdom.getDOMImplementation("").createDocument(None, "doc", None)
    e = document.documentElement
    test(document, e)
    out = pxdom.getDOMImplementation("").createDOMSerializer()
    print out.writeToString(document)
except ImportError:
    print "pxdom not tested."

# vim: tabstop=4 expandtab shiftwidth=4
