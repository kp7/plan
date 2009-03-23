#!/usr/bin/env python

import libxml2dom, xml.dom.minidom

print
print "This is libxml2dom's behaviour for default namespaces:"
print
document = libxml2dom.createDocument(None, "doc", None)
top = document.xpath("*")[0]
elem1 = document.createElementNS("DAV:", "href")
print "Namespace is", repr(elem1.namespaceURI)
document.replaceChild(elem1, top)
elem2 = document.createElementNS(None, "no_ns")
print "Namespace is", repr(elem2.namespaceURI)
document.xpath("*")[0].appendChild(elem2)
print "Find href", len(document.xpath("href")) != 0
print "Find x:href", len(document.xpath("x:href", namespaces={"x": "DAV:"})) != 0
print "Find //no_ns", len(document.xpath("//no_ns")) != 0
print "Find x:href/no_ns", len(document.xpath("x:href/no_ns", namespaces={"x": "DAV:"})) != 0
print document.toString()
document.toFile(open("test_ns.xml", "wb"))

document = libxml2dom.parse("test_ns.xml")
print "Namespace is", repr(document.xpath("*")[0].namespaceURI)
print "Namespace is", repr(document.xpath("*/*")[0].namespaceURI)
print "Find href", len(document.xpath("href")) != 0
print "Find x:href", len(document.xpath("x:href", namespaces={"x": "DAV:"})) != 0
print "Find //no_ns", len(document.xpath("//no_ns")) != 0
print "Find x:href/no_ns", len(document.xpath("x:href/no_ns", namespaces={"x": "DAV:"})) != 0
print document.toString()
print "--------"

print
print "This is minidom's behaviour for default namespaces:"
print
document = xml.dom.minidom.Document()
elem1 = document.createElementNS("DAV:", "href")
print "Namespace is", repr(elem1.namespaceURI)
document.appendChild(elem1)
elem2 = document.createElementNS(None, "no_ns")
print "Namespace is", repr(elem2.namespaceURI)
document.childNodes[0].appendChild(elem2)
print document.toxml()
open("test_ns.xml", "wb").write(document.toxml())

document = xml.dom.minidom.parse("test_ns.xml")
print "Namespace is", repr(document.documentElement.namespaceURI)
print "Namespace is", repr([n for n in document.documentElement.childNodes if n.nodeType == n.ELEMENT_NODE][0].namespaceURI)
print document.toxml()
print "--------"

try:
    from xml.dom.ext import PrettyPrint
    print
    print "This is minidom's behaviour for default namespaces with PrettyPrint from PyXML:"
    print
    document = xml.dom.minidom.Document()
    elem1 = document.createElementNS("DAV:", "href")
    print "Namespace is", repr(elem1.namespaceURI)
    document.appendChild(elem1)
    elem2 = document.createElementNS(None, "no_ns")
    print "Namespace is", repr(elem2.namespaceURI)
    document.childNodes[0].appendChild(elem2)
    PrettyPrint(document)
    PrettyPrint(document, stream=open("test_ns.xml", "wb"))

    document = xml.dom.minidom.parse("test_ns.xml")
    print "Namespace is", repr(document.documentElement.namespaceURI)
    print "Namespace is", repr([n for n in document.documentElement.childNodes if n.nodeType == n.ELEMENT_NODE][0].namespaceURI)
    PrettyPrint(document)

except ImportError:
    print "Prettyprinted document not produced."

# vim: tabstop=4 expandtab shiftwidth=4
