from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, SubmitField,ValidationError
=======
from wtforms import StringField, SubmitField, IntegerField
>>>>>>> eeb3b113f0d2aadaca557e1ec21f174fffeebf0f
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Resumo


class SubmissaoForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    texto = StringField('Texto', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    #co_autor = StringField('Co-Autores', validators=[DataRequired()])
<<<<<<< HEAD
    submit = SubmitField('Submit')

    def validate_titulo(self, field):
        if Resumo.query.filter_by(titulo=field.data).first():
            raise ValidationError('Um resumo de mesmo titulo já cadastrado')
=======
    submit = SubmitField('Submit')
>>>>>>> eeb3b113f0d2aadaca557e1ec21f174fffeebf0f
