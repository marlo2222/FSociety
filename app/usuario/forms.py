from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Usuario

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nome = StringField('Nome', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(),EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirme sua senha')
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('O email ja está sendo usado.')

    def validate_username(self, field):
        if Usuario.query.filter_by(nome=field.data).first():
            raise ValidationError('Nome ja esta em uso.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
