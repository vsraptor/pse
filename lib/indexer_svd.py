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

#import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

class Indexer:

	@staticmethod
	def urls(url_list):
		for url in open(url_list,'r'): yield url.rstrip("\n")

	@staticmethod
	def files(start_dir=Utils.tmp_dir):
		for root,dirs,files in os.walk(start_dir) :
			for f in files : yield open(start_dir + '/' + f,'r').read()

	@staticmethod
	def save2file(name, string):
		with open(name,'w') as txt: txt.write(string)

	def __init__(self,levels=200):
		self.levels = levels
		self.stop_words = get_stop_words('en')
		self.log = Utils.init_logger()


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
		self.log.debug("%s : %s" % (idx, url))
		try:
			#debug = {'verbose': sys.stderr}
			user_agent = {'User-agent': 'Mozilla/5.0'}
			resp = requests.get(url, timeout=10, allow_redirects=True, headers=user_agent)#, config=debug)
			if resp.ok :
				#path = '../tmp/' + str(idx) + '.txt'
				path = "../tmp/%s.txt" % idx
				#content = Document(resp.content).summary()
				content = self.cleanup(resp.content)
				if not content : return None
				Indexer.save2file(path, content)
			else:
				self.log.error("*(%s) %s : %s" % (resp.status_code, resp.reason, resp.headers['Content-Type']))
				return None
		except Exception as e:
			print Exception(e)
			print "Err processing %s" % url

	def svd(self):
		#number of the levels should not exceed any axis lenght of tfidf matrix
		shape_min = min(self.tfidf_matrix.shape)
		levels = self.levels if self.levels < shape_min else shape_min-1
		self.log.debug("svd levels: %s" % levels)
		u,s,vt = svds(self.tfidf_matrix.T,k=levels)
		Utils.npa2file(u,fname='u')
		Utils.npa2file(s,fname='s')
		Utils.npa2file(vt,fname='vt')
		print u
		print s
		print vt

	def build_tfidf(self):
		#!fixme : add steming
		self.tfidf = TfidfVectorizer(min_df=1, use_idf=True, token_pattern=u'[a-zA-Z]{2,}', stop_words=self.stop_words)
		self.tfidf_matrix = self.tfidf.fit_transform(Indexer.files())
		self.log.debug( "tfidf matrix shape> %s " % self.tfidf_matrix.shape )
		Utils.dict2csv(self.tfidf.vocabulary_)
		Utils.npa2file(self.tfidf_matrix.toarray(), fname='tfidf_matrix')


	def process(self):
		for idx, u in enumerate( Indexer.urls(Utils.data_dir + '/url.lst') ) :
			#if idx == 5: break
			self.fetch(u,idx)
		self.build_tfidf()
		self.svd()

