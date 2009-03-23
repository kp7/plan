#!/usr/bin/env python

import libxml2dom.xmpp
import sys

sender = "sender" in sys.argv
receiver = "receiver" in sys.argv
if not (sender or receiver):
    print "Please specify sender or receiver."
    sys.exit(1)

if len(sys.argv) > 2:
    peer = sys.argv[2]
elif sender:
    peer = "paulb@jeremy/receiver"

s = libxml2dom.xmpp.Session(("localhost", 5222))
d = s.connect("jeremy")
print "---- 1 ----"
print d.toString()

auth = s.createAuth()
auth.mechanism = "PLAIN"
auth.setCredentials("paulb@jeremy", "paulb", "jabber")
d = s.send(auth)
print "---- 2 ----"
print d.toString()

d = s.connect("jeremy")
print "---- 3 ----"
print d.toString()

iq = s.createIq()
iq.makeBind()
if sender:
    iq.bind.resource = "sender"
else:
    iq.bind.resource = "receiver"
d = s.send(iq)
print "---- 4 ----"
print d.toString()

iq = s.createIq()
iq.makeSession("jeremy")
d = s.send(iq)
print "---- 5 ----"
print d.toString()

if sender:
    message = s.createMessage()
    message.from_ = "paulb@jeremy/sender"
    message.to = peer
    message.type = "chat"
    message.body = message.createBody()
    text = message.ownerDocument.createTextNode("Hello!")
    message.body.appendChild(text)
    print "Sending..."
    print message.toString()
    d = s.send(message)

if receiver:
    while 1:
        print "Listening..."
        doc = s.receive()
        print doc.toString()
        print
        print "From:", doc.from_
        print "To:", doc.to
        print "Type:", doc.type
        print
        if doc.localName == "message":
            print "Message..."
            if doc.type == "chat" and doc.body:
                print doc.body.textContent
            elif doc.event:
                print "Composing?", doc.event.composing
                print "Delivered?", doc.event.delivered
                print "Displayed?", doc.event.displayed
                print "Offline?", doc.event.offline
                print "Id:", doc.event.id
        elif doc.localName == "presence":
            print "Presence..."
            if doc.type == "subscribe":
                presence = s.createPresence()
                presence.type = "subscribed"
                presence.from_ = doc.to
                presence.to = doc.from_
                print "Sending..."
                print presence.toString()
                d = s.send(presence)
        print

# vim: tabstop=4 expandtab shiftwidth=4
