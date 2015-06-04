import csv
import pickle
import numpy as np
import logging
import os, sys
from os.path import join



class Utils:

	log = None #Logger

	base_dir = os.path.abspath(os.path.dirname(__file__))
	root_dir = os.path.abspath(join(base_dir, '..'));
	data_dir = join(root_dir , 'data')
	tmp_dir  = join(root_dir, 'tmp')
	log_dir  = join(root_dir, 'log')

	@staticmethod
	def init_logger(log_file='indexer.log'):
		if Utils.log : return Utils.log #already initialized
		l = logging.getLogger()
		l.setLevel(logging.DEBUG)
		sth = logging.StreamHandler()
		sth.setLevel(logging.DEBUG)
		fh = logging.FileHandler(join(Utils.log_dir, log_file))
		fh.setLevel(logging.DEBUG)
		l.addHandler(sth)
		l.addHandler(fh)
		#l.basicConfig(level=l.DEBUG, format='>%(message)s')
		Utils.log = l
		return l


	@staticmethod
	def dict2csv(ary, path=None, fname='vocabulary.csv'):
		if not path : path = Utils.data_dir
		w = csv.writer(open(join(path,fname), "w"), lineterminator="\n")
		for key, val in ary.items(): w.writerow([key, val])

	@staticmethod
	def csv2dict(path=None, fname='vocabulary.csv', val_int=True):
		if not path : path = Utils.data_dir
		ary = {}
		for key, val in csv.reader(open( join(path, fname) )):
		    ary[key] = int(val) if val_int else val
		Utils.log.debug("len:%s> %s" % (fname,len(ary)))
		return ary

	@staticmethod
	def pkl2file(data,path=None,dst_file='vocabulary.pkl'):
		if not path : path = Utils.data_dir
		with open(join(path, dst_file), "wb") as f : pickle.dump(data,f)

	@staticmethod
	def file2pkl(path=None,src_file='vocabulary.pkl'):
		if not path : path = Utils.data_dir
		with open(join(path,src_file), "rb") as f : data = pickle.load(f)
		return data

	@staticmethod
	def npa2file(data,fname,path=None):
		Utils.log.debug("shape:%s> %s" % (fname,data.shape))
		if not path : path = Utils.data_dir
		np.save(join(path,fname), data)

	@staticmethod
	def file2npa(fname,path=None):
		if not path : path = Utils.data_dir
		ary = np.load(join(path, fname) )
		Utils.log.debug("shape:%s> %s" % (fname,ary.shape))
		return ary

	@staticmethod
	def key_by_val(d, val):
		for k in d.keys():
			if d[k] == val : return k
		return ""

	@staticmethod
	def is_empty(lst): return not bool(len(lst))

