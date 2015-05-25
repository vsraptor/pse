## Personal Search engine (bookmarks + external search)

### What is this ?

Have you been frustrated having a bootload of quality bookmarks, but whenever you need something it is much faster to
just fire a browser and do a Google search, instead.
You no longer need to do that. Enter the Personal search engine (PSE), which you can use to index your bookmarks and search like 
you do with Google.
But wait there is more, when you issue your search query the PSE in the background does a Google search (or other search if you implemnt it :))
and displays both results.

The code is working but is still in Alpha stage. When it is Beta, I will write an article on http://ifni.co how it works.

### INSTALLATION AND RUNNING

#### Clone the PSE repository

```
> git clone https://github.com/vsraptor/pse.git
> cd pse
```

#### Virtual python enviroment

If you don't want to polute your system-wide python installation do the following, otherwise skip this step.

```
$ # Create virtualenv in home
> virtualenv .myenv
$ # Activate the virtualenv
> source .myenv/bin/activate
```

#### Installation

You would need to install scikit-learn (for Tfidf support) and Flask for the web app

```
> pip install scikit-learn
> pip install flask
> pip install flask-script
> pip install flask-bootstrap
```

#### url.lst

Next either create manually url.lst file in data directory or generate one using bin/bm2urls.py.
Btw url.lst is simply list of URLs.

#### Create the index

Now you have to run the indexer to create the tfidf index matricies.

```
> cd bin
> python idx.py
```

### Run the cmd-line app or the web-app

There cmd line app, mainly for testing purposes.
You can run it like this :

```
> cd bin
> python query.py -b -q 'python loop'
```

Or better run the Web app :

```
> cd site
> python manage.py runserver
```

Then go to the following address :

```
http://localhost:5000
```



