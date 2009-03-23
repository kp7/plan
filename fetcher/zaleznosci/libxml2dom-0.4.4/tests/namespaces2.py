#!/usr/bin/env python

import libxml2dom, xml.dom, xml.dom.minidom

document = libxml2dom.createDocument(None, "doc", None)
top = document.xpath("*")[0]
elem1 = document.createElementNS("DAV:", "myns:href")
elem1.setAttributeNS(xml.dom.XMLNS_NAMESPACE, "xmlns:myns", "DAV:")
elem1.setAttributeNS(xml.dom.XMLNS_NAMESPACE, "xmlns:otherns", "urn")
document.replaceChild(elem1, top)
print document.toString()

document2 = xml.dom.minidom.Document()
elem1 = document2.createElementNS("DAV:", "myns:href")
elem1.setAttributeNS(xml.dom.XMLNS_NAMESPACE, "xmlns:myns", "DAV:")
elem1.setAttributeNS(xml.dom.XMLNS_NAMESPACE, "xmlns:otherns", "urn")
document2.appendChild(elem1)
print document2.toxml()

# vim: tabstop=4 expandtab shiftwidth=4
