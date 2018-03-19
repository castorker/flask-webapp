from flask import Blueprint

quibbles = Blueprint('quibbles', __name__)

from . import views