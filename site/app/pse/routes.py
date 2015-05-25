from flask import render_template, url_for, request, flash
from . import pse

from search import SearchException
from bmark_search import BmarkSearch
from google_search import GoogleSearch
from utils import Utils


@pse.route('/')
def index():
	return render_template('pse/index.html')

@pse.route('/search', methods=['POST','GET'])
def search():
	google = GoogleSearch()
	bmark = BmarkSearch()

	if request.form.has_key('q') :
		q = request.form['q']

		if len(q) > 0 :

			try:
				bmark.search(q)
			except Exception as e :
				flash('Bmark search: ' + e.message)

			try :
				google.search(q)
			except Exception as e:
				flash("Google search error : " + e.message)

		else:
			flash('Interesting what will happen if you search for something rather than nothing !!')

	return render_template('pse/search.html', search=bmark, google=google, query=q)

