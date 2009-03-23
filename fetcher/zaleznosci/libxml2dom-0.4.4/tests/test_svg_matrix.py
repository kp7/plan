#!/usr/bin/env python

import libxml2dom.svg

d = libxml2dom.svg.createSVGDocument()
de = d.documentElement

# Test easy matrices.

m = de.createSVGMatrixComponents(2, 0, 0, 2, 0, 0)
de.setMatrixTrait("test", m)
print de.getAttribute("test")
m2 = de.getMatrixTrait("test")
print "Same matrix?", m == m2
m = de.createSVGMatrixComponents(1, 0, 0, 1, 10, -10)
de.setMatrixTrait("test", m)
print de.getAttribute("test")
m2 = de.getMatrixTrait("test")
print "Same matrix?", m == m2

# Test other operations.

de.setAttribute("test", "rotate(90)")
m = de.getMatrixTrait("test")
de.setMatrixTrait("test", m)
print de.getAttribute("test")
m2 = de.getMatrixTrait("test")
print "Same matrix?", m == m2

# vim: tabstop=4 expandtab shiftwidth=4
