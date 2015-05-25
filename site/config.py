import os, sys

basedir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.abspath(os.path.join(basedir, '../lib'));
sys.path.append(libdir)


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')

class DevConfig(Config):
	DEBUG = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or '123'
#	TFIIDF_FILE = os.environ.get('TFIDF_FILE') or os.path.join(basedir,'/data/tfidf_matrix.npy')
#	VOCABULARY_FILE = os.environ.get('VOCABILARY_FILE') or os.path.join(basedir,'/data/vocabulary.csv')

class ProdConfig(Config):
	pass


config = {
	'develpment' : DevConfig,
	'production' : ProdConfig,
	'default'  : DevConfig
}
