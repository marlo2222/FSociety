from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Resumo


class SubmissaoForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    texto = StringField('Texto', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    #co_autor = StringField('Co-Autores', validators=[DataRequired()])
    submit = SubmitField('Submit')
