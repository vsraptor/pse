#!/usr/bin/env python
import sys
import getopt
sys.path.append('../lib')
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
		print opts
	except getopt.GetoptError:
		print "query.py -b|g|a -q <query>"
		sys.exit(2)
	if opts.has_key('-b') : bmark_search(opts['-q'])
	if opts.has_key('-g') : google_search(opts['-q'])



if __name__ == '__main__' : main(sys.argv[1:])