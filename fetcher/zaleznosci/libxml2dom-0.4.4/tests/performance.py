#!/usr/bin/env python

"""
A performance test using libxml2dom.macrolib, libxml2dom and minidom.
This module must be compiled using libxml2macro.py and run only as a compiled
module - ie. as performance.pyc.
"""

import xml.dom

def find_root(d):
    root = None
    for n in d.childNodes:
        if n.nodeType == xml.dom.Node.ELEMENT_NODE:
            root = n
            break
    return root

import libxml2macro as x2_

def find_root_libxml2macro(x2_d):
    x2_root = None
    for x2_n in x2_d.childNodes:
        if x2_n.nodeType == xml.dom.Node.ELEMENT_NODE:
            x2_root = x2_n
            break
    return x2_root

def test_import_libxml2macro(x2_d):
    x2_d2 = createDocument("nsD", "newdoc", None)
    x2_imported = x2_d.importNode(find_root_libxml2macro(x2_d), 1)
    x2_d2.replaceChild(x2_imported, find_root_libxml2macro(x2_d2))
    return x2_d, x2_d2

def test_import_minidom(d):
    d2 = xml.dom.minidom.getDOMImplementation().createDocument("nsD", "newdoc", None)
    imported = d2.importNode(find_root(d), 1)
    d2.replaceChild(imported, find_root(d2))
    return d, d2

def test_import_libxml2dom(d):
    d2 = libxml2dom.createDocument("nsD", "newdoc", None)
    imported = d2.importNode(find_root(d), 1)
    d2.replaceChild(imported, find_root(d2))
    return d, d2

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) < 3:
        print "Please specify a filename (of a fairly large XML document) and the testing mode."
        print "There are quite a few large files in the libxml2 distribution."
        print "For the testing mode, choose one of libxml2macro, minidom, libxml2dom."
        sys.exit(1)

    if sys.argv[2] == "libxml2macro":

        x2_d = parseFile(sys.argv[1])

        t = time.time()
        x2_d1, x2_d2 = test_import_libxml2macro(x2_d)
        toFile(x2_d2, "/tmp/xxx_libxml2macro.xml")
        print "Time", time.time() - t, "seconds"

    elif sys.argv[2] == "minidom":
        import xml.dom.minidom
        d = xml.dom.minidom.parse(sys.argv[1])

        t = time.time()
        d1, d2 = test_import_minidom(d)
        open("/tmp/xxx_minidom.xml", "wb").write(d2.toxml("utf-8"))
        print "Time", time.time() - t, "seconds"

    elif sys.argv[2] == "libxml2dom":
        import libxml2dom
        d = libxml2dom.parse(sys.argv[1])

        t = time.time()
        d1, d2 = test_import_libxml2dom(d)
        libxml2dom.toStream(d2, open("/tmp/xxx_libxml2dom.xml", "wb"))
        print "Time", time.time() - t, "seconds"

# vim: tabstop=4 expandtab shiftwidth=4
