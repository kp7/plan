#!/usr/bin/env python

"""
The controversial "begat" benchmark. This module must be compiled using
libxml2macro.py before use, and must then be invoked directly as a compiled
module - ie. as begat.pyc.
"""

import libxml2macro as n_

def test_begat_libxml2macro(n_doc, full_xpath):
    l = []

    if full_xpath:
        for n_node in n_doc.xpath("//v[contains(text(), 'begat')]"):
            text = n_node.nodeValue
            l.append(text)
    else:
        # NOTE: Code corresponding to this was suggested for cElementTree, but why not
        # NOTE: take full advantage of XPath if you have most of the code written in C?

        for n_node in n_doc.xpath("//v"):
            text = n_node.nodeValue
            if text.find(u'begat') != -1:
                l.append(text)

    return l

def test_begat_libxml2dom(doc, full_xpath):
    l = []

    if full_xpath:
        for node in doc.xpath("//v[contains(text(), 'begat')]"):
            text = node.nodeValue
            l.append(text)
    else:
        # NOTE: Code corresponding to this was suggested for cElementTree, but why not
        # NOTE: take full advantage of XPath if you have most of the code written in C?

        for node in doc.xpath("//v"):
            text = node.nodeValue
            if text.find(u'begat') != -1:
                l.append(text)

    return l

if __name__ == "__main__":
    import time, os
    import sys

    ot_locations = [arg for arg in sys.argv if arg.endswith("ot.xml")]
    full_xpath = "--full" in sys.argv
    use_libxml2dom = "libxml2dom" in sys.argv
    use_libxml2macro = "libxml2macro" in sys.argv
    iterations = [int(arg.split("-")[0]) for arg in sys.argv if arg.endswith("-times")]

    if len(ot_locations) == 0:
        print "Please specify the location of the ot.xml file."
        sys.exit(1)

    if len(iterations) == 0:
        iterations = 1
    else:
        iterations = iterations[0]

    raw_input("Start your engines with ps -p %s -fv" % os.getpid())
    t = time.time()

    for i in range(0, iterations):
        if use_libxml2macro:
            n_doc = parseFile(ot_locations[0])
            l = test_begat_libxml2macro(n_doc, full_xpath)
        else: # use_libxml2dom:
            import libxml2dom
            doc = libxml2dom.parse(ot_locations[0])
            l = test_begat_libxml2dom(doc, full_xpath)

    print "Time taken", time.time() - t
    raw_input("Stop your engines!")

    print l

# vim: tabstop=4 expandtab shiftwidth=4
