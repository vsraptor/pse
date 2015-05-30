## Personal Search engine
##### Combined Bookmarks and external search

### What is this ?

Aren't you frustrated having a boatload of quality bookmarks, but not using them because it is faster to
just fire a browser and do a Google search, instead ! Yeah, me too !

You no longer need to do that. Enter the Personal search engine (PSE), which you can use to index your bookmarks and search like 
you do with Google.

But wait there is more, when you issue your search query the PSE in the background does a Google search for you (or other search if you implement it :))
and displays both results.

The code is working but is still in Alpha stage. When it is Beta, I will write an article on http://ifni.co how it works.
Below is a quick recepie how to install it and use it.

---

### INSTALLATION AND RUNNING

#### Clone the PSE repository

```
> git clone https://github.com/vsraptor/pse.git
> cd pse
```

#### Virtual python environment

If you don't want to pollute your system-wide python installation do the following, otherwise skip this step.

```
$ # Create virtualenv in home
> virtualenv .myenv
$ # Activate the virtualenv
> source .myenv/bin/activate
```

#### Installation

You would need to install scikit-learn (for Tfidf support) and Flask for the web app

```
> pip install lxml
> pip install numpy
> pip install requests
> pip install stop_words
> pip install scikit-learn
> pip install flask
> pip install flask-script
> pip install flask-bootstrap
```

#### Create url.lst file.

Next either create manually url.lst file in the data directory or generate one using bin/bm2urlst.py.
Btw url.lst is simply list of URLs. (This repo contains one just for tests, but better generate your own
once you have the app running. You can also have empty lines or comment urls with hash so they don't get included in the index)

#### Create the index

Now you have to run the indexer to create the tfidf index matrices.
This will go trough the list of URLs, fetch the pages and create index, which later
you will use to do the searches.

```
> cd bin
> python idx.py
```

### Run the cmd-line app or the web-app

There cmd line app, is mainly for testing purposes.
You can run it like this (-b bookmark search, -g google search) :

```
> cd bin
> python query.py -b -q 'history biology'
```

Or better run the Web app :

```
> cd site
> python manage.py runserver
```

Then go to the following web address :

```
http://localhost:5000
```


#### Converting firefox bookmarks to url.lst

```
> cd bin
> python bm2urlst.py /path/to/bookmarks.html | grep 'png$\|gif$\|jpg$' > ../data/url.lst
```
