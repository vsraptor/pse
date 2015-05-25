from utils import Utils
from query_parser import QueryParser

class Search(object):

	def __init__(self):
		self.log = Utils.init_logger('search.log')
		self.user_agent = {'User-agent': 'Mozilla/5.0'}
		self.results_count = 0


class SearchException(Exception):
	pass
