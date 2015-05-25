#!/usr/bin/env python
import numpy as np
from utils import Utils

class Search:

	def __init__(self):
		self.log = Utils.init_logger()
		self.load_matricies()

	def load_matricies(self):
		self.u = Utils.file2npa(fname='u.npy')
		self.s = Utils.file2npa(fname='s.npy')
		self.vt = Utils.file2npa(fname='vt.npy')
		self.vocabulary = Utils.csv2dict()
		self.tfidf_matrix = Utils.file2npa(fname='tfidf_matrix.npy')

	def build_search_vector(self,word_list):
		query = np.zeros(len(self.vocabulary),dtype=int)
		for word in word_list:
			print word
			if word in self.vocabulary : query[ int(self.vocabulary[word]) ] = 1
		print np.where(query > 0)
		self.log.debug("query shape> %s" % query.shape)
		Utils.npa2file(query,fname='query')
		return query


	def qv2sv(self,query_vector):
		return np.dot( query_vector, np.dot(self.u, np.linalg.inv( np.diag(self.s) )) )
#		return np.dot(self.u, np.linalg.inv( np.diag(self.s) ))

	@staticmethod
	def cosine_similarity(self,vector,matrix):
		sim = ( np.sum(vector*matrix,axis=1) / ( np.sqrt(np.sum(matrix**2,axis=1)) * np.sqrt(np.sum(vector**2)) ) )[::-1]
		return sim

	@staticmethod #calculate Euclidian distance
	def euclidean_distance(vector, matrix):
		dist = np.sqrt(np.sum((vector - matrix)**2,axis=1))
		#dist = np.linalg.norm(vector - matrix, axis=1)
		return dist


	def search(self,query):
		qv = self.build_search_vector(query)
		print np.linalg.inv( np.diag(self.s) )
		print self.qv2sv(qv)

