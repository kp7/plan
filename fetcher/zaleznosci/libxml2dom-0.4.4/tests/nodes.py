#!/usr/bin/env python

"Test of elements and attribute interfaces."

import libxml2macro as n_

try:
    do_not_have_libxml2macro = n_
    import libxml2dom
    use_libxml2dom = 1
except NameError:
    use_libxml2dom = 0

if __name__ == "__main__":
    import sys

    s = "<ddd:doc xmlns:ddd='http://ddd'/>"

    if use_libxml2dom:
        n_d = libxml2dom.parseString(s)
    else:
        n_d = parseString(s)

    n_e = n_d.xpath("*")[0]
    assert n_e.parentNode == n_d
    assert n_e.namespaceURI == "http://ddd"
    assert n_e.nodeName == n_e.tagName == "ddd:doc"
    assert n_e.localName == "doc"
    print n_d.toString()

    n_e.setAttributeNS("http://xxx", "xxx:x", "y")
    assert n_e.getAttributeNS("http://xxx", "x") == "y"
    l = n_e.xpath("@*")
    assert len(l) == 1
    n_a = l[0]
    assert n_a.parentNode == n_e
    assert n_a.namespaceURI == "http://xxx"
    assert n_a.nodeName == "xxx:x"
    assert n_a.localName == "x"
    assert n_a.nodeValue == n_a.value == "y"
    print n_d.toString()

    n_a2 = n_d.createAttributeNS("http://aaa", "aaa:a")
    n_a2.nodeValue = "b"
    assert n_a2.namespaceURI == "http://aaa"
    assert n_a2.nodeName == "aaa:a"
    assert n_a2.localName == "a"
    assert n_a2.nodeValue == n_a2.value == "b"
    print n_d.toString()

    n_e.setAttributeNodeNS(n_a2)
    l2 = n_e.xpath("@*")
    assert len(l2) == 2
    print n_d.toString()

    n_e.setAttributeNS("http://ccc", "ccc:c", "d")
    assert n_e.getAttributeNS("http://ccc", "c") == "d"
    l3 = n_e.xpath("@*")
    assert len(l3) == 3
    n_e.setAttribute("p", "q")
    assert n_e.getAttribute("p") == "q"
    l4 = n_e.xpath("@*")
    assert len(l4) == 4
    al = n_e.attributes
    assert len(al.items()) == 4

    if use_libxml2dom:
        n_a3 = al.getNamedItemNS("http://ccc", "c")
        assert n_a3.namespaceURI == "http://ccc"
        assert n_a3.nodeName == "ccc:c"
        assert n_a3.localName == "c"
        assert n_a3.nodeValue == "d"
        print n_d.toString()

    n_a4 = n_e.createAttribute("m")
    n_a4.nodeValue = "n"
    assert n_a4.namespaceURI == None
    assert n_a4.nodeName == "m"
    assert n_a4.localName == "m"
    assert n_a4.nodeValue == n_a4.value == "n"
    print n_d.toString()

    if use_libxml2dom:
        n_a4_old = al.setNamedItem(n_a4)
        assert n_a4_old == None
        assert len(al.items()) == 5
        assert n_e.getAttribute("m") == "n"
        al.removeNamedItem("m")
        assert not n_e.hasAttribute("m")
        assert len(al.items()) == 4

    n_e.removeAttributeNS("http://ccc", "c")
    assert not n_e.hasAttributeNS("http://ccc", "c")
    l5 = n_e.xpath("@*")
    assert len(l5) == 3
    n_e.removeAttribute("p")
    assert not n_e.hasAttribute("p")
    l6 = n_e.xpath("@*")
    assert len(l6) == 2
    print n_d.toString()

# vim: tabstop=4 expandtab shiftwidth=4
