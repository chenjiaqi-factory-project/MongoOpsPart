from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
mongo = PyMongo(app)

from app import routes, api
