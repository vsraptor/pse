#!/usr/bin/env python
import requests
import re, os
import logging
#from readability.readability import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from lxml import html
from lxml.html.clean import clean_html
from stop_words import get_stop_words
from utils import Utils
from scipy.sparse.linalg import svds
from os import listdir
from os.path import isfile, join

#import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

class Indexer:

	@staticmethod
	def urls(url_list):
		for url in open(url_list,'r'):
			#empty string or comment
			if not url.strip() or url.strip().startswith('#') : continue
			yield url.rstrip("\n")


	@staticmethod
	def save2file(name, string):
		with open(name,'w') as txt: txt.write(string)

	def __init__(self,levels=200):
		self.levels = levels
		self.stop_words = get_stop_words('en')
		self.log = Utils.init_logger()
		self.doc_idx = 0 #current doc index
		self.doc_urls = {}

	def cleanup(self,string):
#		string = html.clean.clean_html(string)
		dom = html.fromstring(string)
		for tag in ( "script", "style", "form", "iframe", "textarea", "a") :
			for i in dom.xpath('//'+tag): i.drop_tree()
		body = dom.xpath('//body')
		if not len(body) : body = dom.xpath('//html')
		if not len(body) :
			self.log.info('*** The page has no <body> tag, skipping ... ***')
			return None
		txt = body[0].text_content().encode(errors='ignore') #encode('utf-8')
		txt = re.sub('\s*\n\s*', '\n', txt)
		txt = re.sub('[ \t]{2,}', ' ', txt)
		if not txt : self.log.error("Empty html")
		return txt.strip()

	def fetch(self,url,idx):
		self.log.debug("%s : (%s) %s" % (self.doc_idx, idx, url))
		try:
			#debug = {'verbose': sys.stderr}
			user_agent = {'User-agent': 'Mozilla/5.0'}
			resp = requests.get(url, timeout=10, allow_redirects=True, headers=user_agent)#, config=debug)
			if resp.ok :
				path = "../tmp/%s.txt" % self.doc_idx
				#content = Document(resp.content).summary()
				content = self.cleanup(resp.content)
				if not content : return None
				Indexer.save2file(path, content)
				self.doc_urls[self.doc_idx] = url #collect the urls
				self.doc_idx += 1 #inc only on success
			else:
				self.log.error("*(%s) %s : %s" % (resp.status_code, resp.reason, resp.headers['Content-Type']))
				return None
		except Exception as e:
			print Exception(e)
			print "Err processing %s" % url


	def files(self,start_dir=Utils.tmp_dir):
		for f in self.file_list :
			print "tfidf processing: %s" % f
			yield open(start_dir + '/' + f,'r').read()


	#the file list has to be in numerical order (so that tfidf matrix doc idx follow fetch sequence) otherwise indexing goes out of touch
	def build_file_list(self,start_dir=Utils.tmp_dir):
		files = [ int(f.split('.')[0]) for f in listdir(start_dir) if isfile(join(start_dir,f)) and f.endswith('.txt') ]
		files.sort()
		#!fixme : check for gaps
		self.file_list = [ str(f) + ".txt" for f in files ]

	def build_tfidf(self):
		#!fixme : add steming
		self.tfidf = TfidfVectorizer(min_df=1, use_idf=True, token_pattern=u'[a-zA-Z]{2,}', stop_words=self.stop_words)
		self.tfidf_matrix = self.tfidf.fit_transform(self.files())
		Utils.dict2csv(self.tfidf.vocabulary_, fname='vocabulary.csv')
		Utils.npa2file(self.tfidf_matrix.toarray(), fname='tfidf_matrix')

	def cleanup_old_files(self):
		import glob
		self.log.debug("Cleaning up : " + Utils.tmp_dir)
		files = glob.glob(Utils.tmp_dir + "/*")
		for f in files : os.remove(f)

	def process(self):
		self.cleanup_old_files()
		for idx, u in enumerate( Indexer.urls(Utils.data_dir + '/url.lst') ) :
			#if idx == 10: break
			self.fetch(u,idx)
		self.build_file_list()
		self.build_tfidf()
		#finaly save the url list to csv file
		Utils.dict2csv(self.doc_urls, fname='doc_urls.csv')


