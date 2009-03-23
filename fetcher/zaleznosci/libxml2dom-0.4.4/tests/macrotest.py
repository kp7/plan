#!/usr/bin/env python

"""
A test of macros. This file must be compiled using libxml2macro.py. It may then
be imported normally in Python, but if run then the compiled module should be
invoked directly - ie. as macrotest.pyc.
"""

import libxml2macro as x2_
import xml.dom

class Container:
    pass

doc = """<?xml version="1.0"?>
<doc>
    <element attr="value">
        <subelement/>
    </element>
</doc>
"""

def find_root(x2_d):
    x2_root = None

    # Property access should be transformed.

    for x2_n in x2_d.childNodes:
        if x2_n.nodeType == xml.dom.Node.ELEMENT_NODE:
            x2_root = x2_n
            break

    return x2_root

def test():
    global doc

    # Assignment should not be transformed.

    x2_d = parseString(doc)
    return process(x2_d)

def test_file(filename):

    # Assignment should not be transformed.

    x2_d = parseFile(filename)
    return process(x2_d)

def process(x2_d):

    # Not even within containers, and not special names alone.

    c = Container()
    c.x2_d = x2_d

    # Find the root element.

    x2_root = find_root(x2_d)
    c.x2_root = x2_root

    # Create new attributes.
    # Method access should be transformed.

    x2_root.setAttributeNS("ns", "xxx:yyy", "zzz")
    c.x2_root.setAttributeNS("ns", "XXX:YYY", "ZZZ")

    # Create new elements.
    # Method access should be transformed.

    x2_new = x2_d.createElementNS("ns2", "ppp:qqq")
    x2_root.appendChild(x2_new)
    x2_new2 = c.x2_d.createElementNS("ns2", "PPP:QQQ")
    c.x2_root.appendChild(x2_new2)

    # Create new elements using ownerDocument.
    # Chaining properties is not

    x2_new3 = x2_new.ownerDocument.createElement("fff")
    x2_new.appendChild(x2_new3)
    x2_new4 = x2_new2.ownerDocument.createElement("FFF")
    x2_new2.appendChild(x2_new4)

    return x2_d

def test_import(x2_d):

    # Change the prefix.

    import libxml2macro as node_
    node_d = x2_d

    node_root = find_root(node_d)

    # Create a new document.

    node_d2 = createDocument("nsD", "newdoc", None)
    node_root2 = find_root(node_d2)

    # Attempt to import nodes from the original document.

    node_imported = node_d2.importNode(node_root, 1)
    node_d2.replaceChild(node_imported, node_root2)

    return node_d, node_d2

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print "Running a simple test on", sys.argv[1]
        test_file(sys.argv[1])
    else:
        print "Running a simple test on some built-in string."
        test()

# vim: tabstop=4 expandtab shiftwidth=4
