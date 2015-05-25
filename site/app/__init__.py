from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap()

def create_app(cfg_name):
	app = Flask(__name__)
	app.config.from_object(config[cfg_name])

	from .pse import pse as pse_blueprint
	app.register_blueprint(pse_blueprint)

	bootstrap.init_app(app)

	return app