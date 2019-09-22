from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
mongo = PyMongo(app)

# blueprint for water part
from app.water import bp as water_bp
app.register_blueprint(water_bp, url_prefix='/api/water')

from app import routes, gas_api
