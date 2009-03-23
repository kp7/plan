#!/usr/bin/python
# -*- coding: iso-8859-2 -*-

from xml.dom.ext.reader import HtmlLib
from xml.dom.ext import PrettyPrint

from HTMLParser import HTMLParser
from sgmllib import SGMLParser


import libxml2dom
import re
import urllib2
import time
import os
import pickle
import socket
import sys
import locale

import sys
import codecs

from http import *
from models import *

#if not sys.stdout.encoding:
#sys.stdout = codecs.getwriter('latin2')(sys.stdout)

from ctypes import pythonapi, py_object, c_char_p
PyFile_SetEncoding = pythonapi.PyFile_SetEncoding
PyFile_SetEncoding.argtypes = (py_object, c_char_p)
if not PyFile_SetEncoding(sys.stdout, "latin2"):
    raise ValueError

locale.setlocale(locale.LC_CTYPE, 'pl_PL')

base_url = "http://wazniak.mimuw.edu.pl"


def enc(unicode):
    if not unicode:
	return unicode
    try:
        return unicode.encode('iso-8859-2', 'replace')
    except UnicodeDecodeError:
	return "invalid unicode string"
def extension(link):
    l = len(link)
    p = l-1
    while p>=0 and p>=l-10:
	if link[p]=='.':
	    return link[p+1:].lower()
	p-= 1
    return None
def absolute_url(url):
    if url and url[0]=='/':
	url = base_url+url
    return url

def parse( html_data, header):
    class St: pass
    st = St()
    st.id=-1
    st.level = 0
    st.saved_id = -100
    st.saved_level = -1
    st.results = []
    st.used = False
    def check_header( h):
	if header.__class__==str:
	    return h.strip()==header.strip()
	else:
	    return header( h)
    def dfs(node, good_ol=False):
	st.id+= 1
	st.level+= 1
	#print str(node.name) +" " + str(st.id)
#	print "name=%s id=%d content=%s" %( node.name, st.id, node.textContent)
	if ["h2", "h3"].count(enc(node.name)) and check_header( enc(node.textContent)):
	    st.saved_id = st.id
	    st.saved_level = st.level
	    st.used = False
	elif ["ol", "ul"].count( node.name) and (st.id==st.saved_id+3 or st.level==st.saved_level):
	    good_ol = True
	elif st.level==st.saved_level and node.name!="text" and st.used:
	    #print "clearing for item type %s" %(node.name,)
	    st.saved_level = -1
	elif st.level<st.saved_level:
	    st.saved_level = -1
	if node.name=="a" and good_ol:
	    class C: pass
	    c = C()
	    c.link=absolute_url(node.getAttribute('href'))
	    c.name=node.textContent.strip()
	    st.results.append(c)
	    st.used = True
	for x in node.childNodes:
	    dfs( x, good_ol)
	st.level-= 1

    dom = libxml2dom.parseString( html_data, html=True, htmlencoding='utf-8')
    dfs( dom)
    return st.results


def index_test():
    html_data = fetch_html('http://wazniak.mimuw.edu.pl/index.php?title=Strona_g%C5%82%C3%B3wna')
    def check_stage(h):
	return [" Pierwszy stopień ", " Drugi stopień "].count(h)
    for entry in parse( html_data, check_stage):
	print "link=%s, name=%s" %(entry.link,entry.name,)
	html_data2 = fetch_html(entry.link)
	def check_h(h):
	    if h.strip()=="Moduły":
		return True
	    if h.strip()=="Wykłady":
		return True
	    return False
	for entry in parse( html_data2, check_h):
	    if re.search(r'(?M)^(ćwiczenia|Ćwiczenia|test|flash|PDF|PDF kolor|Laboratorium \(PDF\)|PDF-kolor|swf|pdf|pdf kolor|Pytania|pracownicy.sql|pytania|PDF-czb|Laboratorium.*|Ćwiczenia:.*|Ćwiczenie.*|.*\.pdf)$'.lower(), enc(entry.name).lower()):
		continue
	    if ['pdf','doc','zip','java','ppt','sql'].count( extension( entry.link)):
		continue
	    e = enc(entry.name)
	    print " - name='%s'" %(e,)

def build_course( name, url):
    course=Course()
    course.name = name
    course.link = url
    course.lectures = []
    html_data2 = fetch_html(url)
    def check_h(h):
	if h.strip()=="Moduły":
	    return True
	if h.strip()=="Wykłady":
	    return True
	return False
    for entry in parse( html_data2, check_h):
	if re.search(r'(?M)^(ćwiczenia|Ćwiczenia|test|flash|PDF|PDF kolor|Laboratorium \(PDF\)|PDF-kolor|swf|pdf|pdf kolor|Pytania|pracownicy.sql|pytania|PDF-czb|Laboratorium.*|Ćwiczenia:.*|Ćwiczenie.*|.*\.pdf)$'.lower(), enc(entry.name).lower()):
	    continue
	if ['pdf','doc','zip','java','ppt','sql'].count( extension( entry.link)):
	    continue
	course.lectures.append( build_lecture(entry.name, entry.link))
    return course

def build_courses():
    courses = []
    html_data = fetch_html('http://wazniak.mimuw.edu.pl/index.php?title=Strona_g%C5%82%C3%B3wna')
    def check_stage(h):
	return [" Pierwszy stopień ", " Drugi stopień "].count(h)
    entries = parse( html_data, check_stage)
    cur = 0
    for entry in entries:
	courses.append( build_course( entry.name, entry.link))
	cur+=1
	sys.stderr.write("Built course %d/%d\n" %(cur, len(entries)))
    return courses

def get_lecture_text( html_data):
    def try_toc_format( dom):
	def dfs( node):
	    count = None
	    if node.getAttribute("id")=="bodyContent":
		count = 0
	    for x in node.childNodes:
		r = dfs( x)
		if r:
		    return r
		if count!=None:
		    count+= 1
	    return count
	res = ""
	entries = parse( html_data, 'Spis treści')
	#d = dfs(dom)
	#print "dfs returned %d, len(entries)=%d" %(d, len(entries))
	#print "html_data: " + html_data
	if [19,22].count(dfs( dom))==0 or len(entries)<5:
	    return None
	for entry in entries:
	    #print "subentry: %s %s" %(enc( entry.name), enc( entry.link))
	    html_data2 = fetch_html( absolute_url( entry.link))
	    res+= " " + get_lecture_text( html_data2)
	return res
    def dfs(node, good_ol=False):
	if node.getAttribute('id')=='bodyContent':
	    good_ol = True
	if good_ol and node.name=="text":
	    st.results+= " " + enc(node.textContent)
	for x in node.childNodes:
	    dfs( x, good_ol)
    class St: pass
    st = St()
    st.results = ""

    dom = libxml2dom.parseString( html_data, html=True, htmlencoding='utf-8')
    res = try_toc_format(dom)
    if res:
	return res
    dfs( dom)
    return st.results
def build_lecture( text):
    lecture = Lecture()
def build_lecture( name, url):
    lecture = Lecture()
    lecture.name = name
    lecture.link = url
    lecture.words = {}

    html_data = fetch_html(url)
    #print "lecture from: %s" %(url,)
    raw_words = re.findall('(?L)\\w+', get_lecture_text( html_data))

    for w in raw_words:
	word = w.lower()
	lecture.words[word] = lecture.words.get(word, 0)+1
    return lecture
def content_test():
    lecture = build_lecture("Wstęp do algorytmów", 
	    "http://wazniak.mimuw.edu.pl/index.php?title=Wst%C4%99p_do_programowania/Wst%C4%99p_do_algorytm%C3%B3w")
    print lecture.words
def overall_test():
    courses = build_courses()
    for course in courses:
	print "* %s" %(enc(course.name),)
	for lecture in course.lectures:
	    totwords = 0
	    for w,c in lecture.words.iteritems():
		totwords+= c
	    print " - %5d (%5d) words (distinct). Name: %s" %( totwords, len(lecture.words), enc(lecture.name), )

def lect_test():
    html_data = fetch_html('http://wazniak.mimuw.edu.pl/index.php?title=SO-1st-2.3-w12.tresc-1.0-toc')
    entries = parse( html_data, 'Spis treści')
    print "entries:"
    print entries

overall_test()   
#lect_test()

