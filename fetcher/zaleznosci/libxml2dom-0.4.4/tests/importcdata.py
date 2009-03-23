#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import libxml2dom
d = libxml2dom.parseString("""<?xml version='1.0' encoding="iso-8859-15"?>
<doc>
  <![CDATA[I am the character data champion! æøåÆØÅ]]>
</doc>
""")
d2 = libxml2dom.createDocument("http://www.w3.org/1999/xhtml", "html",
    libxml2dom.createDocumentType("html", "-//W3C//DTD XHTML 1.1//EN", "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"))
doc = d.xpath("doc")[0]
doc2 = d2.importNode(doc, 1)
html = d2.xpath("*")[0]
html.appendChild(doc2)

print d2.toString("iso-8859-15")

# vim: tabstop=4 expandtab shiftwidth=4
