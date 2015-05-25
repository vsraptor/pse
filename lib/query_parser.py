import re
from utils import Utils

class QueryParser:

	def __init__(self):
		self.cleanup()

	def cleanup(self):
		self.match_all = False
		self.words = []
		self.except_words = []
		self.have_except_words = False

	def parse(self, query):
		self.cleanup() #reset
		self.query_str = query
		#remove quotes you may have used for Google search
		query = re.sub(r'"','',query)
		if re.search(r'\+', query) :
			self.match_all = True
			query = re.sub('\+','',query)
		lst = query.split()
		for el in lst :
			if el.startswith('-') : self.except_words.append(el.lstrip('-'))
			else : self.words.append(el)
		if not Utils.is_empty(self.except_words) : self.have_except_words = True

if __name__ == '__main__' :
	qp = QueryParser()
	qp.parse('test python')