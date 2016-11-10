import pymongo, sys

from flask import Flask
from pymongo import MongoClient

from app.main.controllers import main
from app.classify.controllers import classify
from app.data.controllers import data

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.WARNING)
logging.getLogger(__name__).addHandler(NullHandler())

# create flask app
app = Flask(__name__)

# load configurations
app.config.from_object('config')

# set blueprints
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(classify, url_prefix='/classify')
app.register_blueprint(data, url_prefix='/data')

# set mongo database
mongo = MongoClient(host=app.config['MONGO_HOST'], port=app.config['MONGO_PORT'], serverSelectionTimeoutMS=app.config['MONGO_TIMEOUT'])
app.database = mongo[app.config['MONGO_DBNAME']]

# check mongo connection
try:
    logging.info(mongo.server_info())
except pymongo.errors.ServerSelectionTimeoutError as err:
    logging.error('Mongo: '+str(err))
    sys.exit()
