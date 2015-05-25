#!/usr/bin/env python
import os, sys
basedir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.abspath(os.path.join(basedir, '../lib'));
sys.path.append(libdir)

from indexer import Indexer

if __name__ == '__main__' :
	ix = Indexer()
	ix.process()
