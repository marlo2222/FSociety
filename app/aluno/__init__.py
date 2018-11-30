from flask import Blueprint

aluno = Blueprint('aluno', __name__)

from . import views
