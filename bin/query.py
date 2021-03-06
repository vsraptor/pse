#!/usr/bin/env python
import getopt
import os, sys
basedir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.abspath(os.path.join(basedir, '../lib'));
sys.path.append(libdir)

from bmark_search import BmarkSearch
from google_search import GoogleSearch

def google_search(query):
	s = GoogleSearch()
	s.search(query)
	for info in s.results() :
		print '-' * 50
		print info
		print s.excerpt(info['id'],5,50)

def bmark_search(query):
	s = BmarkSearch()
	s.search(query)
	for info in s.results() :
		print '-' * 50
		print info
		print s.excerpt(info['id'],5,50)


def main(arguments):
	opts = {}
	try:
		for arg,opt in getopt.getopt(arguments,'gbaq:')[0] : opts[arg] = opt
	except getopt.GetoptError:
		print "query.py -b|g|a -q <query>"
		sys.exit(2)
	if opts.has_key('-b') : bmark_search(opts['-q'])
	if opts.has_key('-g') : google_search(opts['-q'])



if __name__ == '__main__' : main(sys.argv[1:])