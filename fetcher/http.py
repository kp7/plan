#!/usr/bin/python
import urllib2
import re
import os
import sys

class Cache:
    def __init__(self):
	self.dir='cache_data'
    def __url_to_file( self, url):
	return "%s/%s" %( self.dir, re.sub(r'[^a-zA-Z0-9]', '_', url))
    def get( self, url):
	fn = self.__url_to_file( url)
	if os.path.exists( fn):
	    f = open( fn)
	    res = f.read()
	    f.close()
	    return res
	return None
    def put( self, url, data):
	if not os.path.exists( self.dir):
	    os.mkdir(self.dir)
	fn = self.__url_to_file( url)
	f=open( fn, 'w')
	f.write( data)
	f.close()


cache = Cache()
def fetch_html(url):
    res = cache.get( url)
    if res:
	return res

    user_agent = 'AlgoInternetowy Superbot'
    headers = { 'User-Agent' : user_agent }
    sys.stdout.write('Fetching %s\n' %(url,))
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    data = response.read()
    cache.put( url, data)
    return data
