from flask import Blueprint

bp = Blueprint('gas', __name__)

from app.gas import routes
