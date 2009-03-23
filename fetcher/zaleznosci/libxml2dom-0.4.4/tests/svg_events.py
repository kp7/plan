#!/usr/bin/env python

"""
A test of SVG events using somewhat modified and fixed versions of various W3C
examples and a tentative event handler initialisation mechanism.

The specifications are explicit about things like .jar files and inline scripts,
but remain vague about some of the mechanisms. Moreover, the initialiser
interface appears to be part of the "global" object, yet treatment of that
object is also vague, and the specifications focus on plugging in arbitrary
initialisers via .jar files and their metadata.
"""

import libxml2dom.svg

s = """\
<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny"
     xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 500 500">
  <script type="application/x-python" xlink:href=""/>
  <g xml:id="group1" fill="red">
    <rect xml:id="therect" x="0" y="0" width="100" height="100"/>
  </g>
</svg>
"""

class Global(libxml2dom.svg.SVGGlobal):

    "An event handler initialiser for the above document."

    def initializeEventListeners(self, scriptElement):
        document = scriptElement.ownerDocument
        rect = document.getElementById("therect")
        rect.addEventListenerNS(libxml2dom.events.XML_EVENTS_NAMESPACE, "click", Handler(), 0, None)
        g = document.getElementById("group1")
        g.addEventListenerNS(libxml2dom.events.XML_EVENTS_NAMESPACE, "click", Handler(), 0, None)

class Impl(libxml2dom.svg.SVGImplementation):

    "A special implementation referring to the above global class."

    def get_global(self, doc):
        return Global(doc)

class Handler:

    "An event handler."

    def handleEvent(self, event):
        print "Event handled in", event.currentTarget.localName, "in phase", event.eventPhase

d = libxml2dom.svg.parseString(s, impl=Impl())
rect = d.getElementById("therect")
event = d.createEvent("MouseEvent")
event.initEventNS(libxml2dom.events.XML_EVENTS_NAMESPACE, "click", 1, 1)
event.detail = "1"
d.sendEventToTarget(event, rect)

s2 = """\
<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny"
     xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 500 500"
     xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:exns="http://example.org/exNS">
  <script xml:id="init" type="application/x-python" xlink:href=""/>
  <g xml:id="group1" fill="red">
    <handler type="application/x-python" ev:event="click" ev:phase="capture" xlink:href="#init" exns:listenerClass="Handler"/>
    <rect xml:id="therect" x="0" y="0" width="100" height="100">
      <handler type="application/x-python" ev:event="click" xlink:href="#init" exns:listenerClass="Handler"/>
    </rect>
  </g>
</svg>
"""

class Global2(libxml2dom.svg.SVGGlobal):

    "An event handler initialiser for the above document."

    def createEventListener(self, handlerElement):
        listenerInstance = None
        try:
            listenerClass = handlerElement.getAttributeNS("http://example.org/exNS", "listenerClass")
            listenerInstance = globals()[listenerClass]()
        except:
            pass
        return listenerInstance

class Impl2(libxml2dom.svg.SVGImplementation):

    "A special implementation referring to the above global class."

    def get_global(self, doc):
        return Global2(doc)

d2 = libxml2dom.svg.parseString(s2, impl=Impl2())
rect2 = d2.getElementById("therect")
event2 = d2.createEvent("MouseEvent")
event2.initEventNS(None, "click", 1, 1)
event2.detail = "1"
d2.sendEventToTarget(event2, rect2)

# vim: tabstop=4 expandtab shiftwidth=4
