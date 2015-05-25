#!/usr/bin/env python
import sys
sys.path.append('../lib')
from indexer import Indexer

if __name__ == '__main__' :
	ix = Indexer()
	ix.process()
