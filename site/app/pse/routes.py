from flask import render_template, url_for, request, flash
from . import pse
from flask import g

import os, sys
libdir = os.path.abspath('../lib');
sys.path.append(libdir)
from search import SearchException
from bmark_search import BmarkSearch
from google_search import GoogleSearch
from utils import Utils


@pse.route('/')
def index():
	return render_template('pse/index.html')

@pse.route('/search', methods=['POST','GET'])
def search():
	#g.log = Utils.init_logger('search.log')
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

