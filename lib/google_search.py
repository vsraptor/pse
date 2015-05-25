import requests
import re
import lxml.html as lh
from lxml import etree
from utils import Utils
from search import Search, SearchException

class GoogleSearch(Search):

	def __init__(self):
		#super(self.__class__,self)
		Search.__init__(self)
		self.qurl = "http://www.google.com/search?hl=en&q="
		self.urls = []
		self.excerpts = []

	def search(self,query):
		#if isinstance(query,list) : query = ' '.join(query)
		query = re.sub(r'\+','', query) #remove + you may have used for bmark search
		url = self.qurl + query
		print url
		resp = requests.get(url, timeout=10, allow_redirects=True, headers=self.user_agent)#, config=debug)
		if resp.ok :
			#with open(Utils.tmp_dir + '/google.html', 'w') as html : print html.write(resp.content)
			doc = lh.fromstring(resp.content)
			results = doc.xpath('//li[@class="g"]')
			#results = doc.xpath('//li[@class="g" and string-length(@class) = 1]')
			self.results_count = len(results)
			for r in results :
				url = r.xpath(".//h3[@class='r']/a")
				el = { 'url' : url[0].get('href'), 'text' : url[0].text_content() } if len(url) > 0 else {'url':'??','text':'??'}
				self.urls.append(el)
				ex = r.xpath('.//span[@class="st"]')
				txt = ex[0].text_content() if len(ex) > 0 else ''
				self.excerpts.append(txt)

	def doc_info(self,idx):
		url = 'http://www.google.com' + self.urls[idx]['url']
		url_text = self.urls[idx]['text'] #.text_content() or ''
		info = { 'id' : idx, 'url' : url, 'url_text' : url_text, 'score': 0 }
		return info

	def excerpt(self,idx,num_lines=10,char_count=None):
		rv = self.excerpts[idx] #if idx <= len(self.excerpts) else ''
		return rv

	def results(self,limit=10):
		for idx in range(self.results_count) : yield self.doc_info(idx)


if __name__ == '__main__' :
	gs = GoogleSearch()
	gs.search(['test'])