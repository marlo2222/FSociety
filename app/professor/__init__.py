from flask import Blueprint

professor = Blueprint('professor', __name__)

from . import views
