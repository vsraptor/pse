#!/usr/bin/env python
import numpy as np
from utils import Utils
from search import Search, SearchException
from query_parser import QueryParser
import os.path

class BmarkSearch(Search):

	@staticmethod
	def cosine_similarity(vector,matrix):
		sim = np.sum(vector*matrix,axis=1) / ( np.sqrt(np.sum(matrix**2,axis=1)) * np.sqrt(np.sum(vector**2)) )
		return np.arccos(sim)

	@staticmethod #calculate Euclidian distance
	def euclidean_distance(vector, matrix):
		dist = np.sqrt(np.sum((vector - matrix)**2,axis=1))
		#dist = np.linalg.norm(vector - matrix, axis=1)
		return dist

	def __init__(self):
		#super(self.__class__,self).__init__()
		Search.__init__(self)
		self.load_matricies()
		self.qp = QueryParser()

	def load_matricies(self):
		self.vocabulary = Utils.csv2dict()
		self.tfidf_matrix = Utils.file2npa(fname='tfidf_matrix.npy')
		self.doc_urls = Utils.csv2dict(fname='doc_urls.csv',val_int=False)

	def build_search_vector(self):
		self.query = np.ones(self.query_len,dtype=float)
		return self.query

	#pick only the docs that contain words that are in the query
	def match_docs(self):
		self.matched_docs = []
		self.word_list = [ w.lower() for w in self.qp.words if w in self.vocabulary ]
		#extract the word indecies
		self.word_idxs = [ int(self.vocabulary[word]) for word in self.word_list ]

		#the query is as long as the number of words that appear both in the query and the vocabulary
		self.query_len = len(self.word_idxs)
		if self.query_len == 0 : raise SearchException("Empty query, no match found in the vocabulary for the word you are searching for")

		#pick only documents that contain the query words
		#all words should have a tfidf-score > 0 to be included in the final list
		by_words = np.nonzero( self.tfidf_matrix[:, self.word_idxs ] )[0]
		if self.qp.match_all : #all the words
			#get all ids (matches[0]) and in how many docs they appear (matches[1])
			matches = np.unique( by_words, return_counts=True )
			#pick only those who have query-len number of matching words
			self.matched_docs = matches[0][ np.where(matches[1] == self.query_len)[0] ]
			#print "matched docs>", self.matched_docs
		else : #any of the words
			self.matched_docs = np.unique(by_words)

		#now if there is exclusion words, remove any document from the result that contains those words
		if self.qp.have_except_words :
			self.except_word_list = [ w.lower() for w in self.qp.except_words if w in self.vocabulary ]
			self.except_word_idxs = [ int(self.vocabulary[word]) for word in self.except_word_list ]
			#get the doc idxes which contain words from exclusion list
			doc_exc_ixs = np.nonzero(self.tfidf_matrix[:, self.except_word_idxs ] != 0)[0]
			#print "exc docs> %s" % doc_exc_ixs
			self.matched_docs = np.setdiff1d(self.matched_docs, doc_exc_ixs)

		return self.matched_docs

	def order_matched_by_score(self):
		#filter to only include the matched docs and words
		self.search_matrix = self.tfidf_matrix[ np.ix_(self.matched_docs, self.word_idxs) ]
		#calculate scores
		self.scores = BmarkSearch.cosine_similarity(self.query, self.search_matrix)
		#print "scores> %s" % self.scores
		self.matched_order = np.argsort(self.scores) #idx reflect matched ary, not tfidf matrix
		return self.matched_order

	def order_by_score(self):
		self.order_matched_by_score()
		#this is indexes of the tfidf-matrix, not matched_docs 
		self.idx_by_score =  (self.matched_docs[self.matched_order]) #!if no arccos() => [::-1]
		self.results_count = len(self.idx_by_score)
		return self.idx_by_score

	def search(self,query):
		self.qp.parse(query)

		#limit search only on the specific words and documents that contain them
		self.match_docs()
		self.build_search_vector()
		#generate idxs of the documents sorted by cosine similarity
		self.order_by_score()


#=== For consumption by the UI/Presentation layer

	def query_words(self):
		tmp = []
		for i in range(self.query_len) :
			tmp.append( self.word_list[i] + '(' + str(self.word_idxs[i]) + ')' )
		return ', '.join(tmp)

	def result_doc_ids(self, limit=10): return self.idx_by_score[:limit]
	def doc_info(self, idx):
		url = self.doc_urls[str(idx)]
		#find the correct score, given tfidf-idx i.e. tfidf-idx => matched_docs-idx
		idx_by_val = np.where(self.matched_docs == idx)[0][0]
		score = self.scores[idx_by_val]
		info = {	'id' : idx, 'url' : url, 'score' : score, 'url_text' : url }
		return info

	def excerpt(self,idx,num_lines=10,char_count=None):
		file_name = os.path.join(Utils.tmp_dir, str(idx) + ".txt")
		head = ''
		with open(file_name,"r") as txt :
			for x in range(num_lines) : head += txt.read()
		if char_count == None : return head
		else : return head[:char_count]

	def results(self,limit=10):
		for idx in self.result_doc_ids(limit) : yield self.doc_info(idx)



"""
	def old_order_matched_by_score(self):
		#filter to only include the matched docs and words
		self.search_matrix = self.tfidf_matrix[ np.ix_(self.matched_docs, self.word_idxs) ].copy()
		#self.search_matrix[ self.search_matrix == 0 ] = -1

		#calculate scores
		self.ed = BmarkSearch.euclidean_distance(self.query, self.search_matrix)
		#np.ones(self.search_matrix.shape[0]) #
		self.cs = BmarkSearch.cosine_similarity(self.query, self.search_matrix)
		self.scores = np.vstack((self.cs,self.ed))

		#sort by first then by second column
		# x[ lexsort((x[:,1],x[:,0])) ]
		#sort by 'cs' row, then by 'ed' row
		self.matched_order = np.lexsort((self.scores[1,:], self.scores[0,:] )) #idx reflect mathed ary, not tfidf matrix
		print "m order> %s" % self.matched_order
		return self.matched_order

"""
