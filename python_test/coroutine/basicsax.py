#!/usr/bin/env python
# coding=utf-8
import xml.sax

class MyHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        print "start Element", name

    def endElement(self, name):
        print "endElement", name

    def characters(self, text):
        print "characters", repr(text)[:40]


xml.sax.parse("example.xml", MyHandler())
