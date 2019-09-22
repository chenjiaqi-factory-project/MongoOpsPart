from flask import Blueprint

bp = Blueprint('elec', __name__)

from app.elec import routes
