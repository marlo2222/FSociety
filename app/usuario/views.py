from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
import re

from . import usuario
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Usuario

@usuario.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if verificaNome(form.username.data):
            if verificaSenha(form.password.data):
                usuario = Usuario(email=form.email.data,username=form.username.data,password=form.password.data)
                if verificarEmail(form.email.data):
                    db.session.add(usuario)
                    db.session.commit()
                    flash('You have successfully registered! You may now login.')
                else:
                    usuario.is_prof = True
                    db.session.add(usuario)
                    db.session.commit()
                    flash('You have successfully registered! You may now login.')
            else:
                flash('Sua senha é ruim')
        else:
            flash('Nome de usuario invalido')
        return redirect(url_for('usuario.login'))

    return render_template('usuario/register.html', form=form, title='Register')

def verificaNome(self,field):
    string = field.data
    result = re.search(r"/d", string,re.MULTILINE)
    if result == None:
        return True
    return False

def verificaSenha(self,field):
    string = field.data
    if len(string) >= 8:
        result = re.search(r"/W", string,re.MULTILINE)
        if result == None:
            return True
        return False
    return False

def verificarEmail(self,field):
    string1 = field
    result = re.search(r"alu.ufc.com", string,re.MULTILINE)
    if result == None:
        return True
    else:
        return False


@usuario.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario is not None and usuario.verify_password(form.password.data):
            login_user(usuario)

            if usuario.is_professor:
                #falta troca
                return redirect(url_for('main.professor_dashboard'))
            else:
                #falta trocar
                return redirect(url_for('main.dashboard'))

        else:
            flash('Invalid email or password.')

    return render_template('usuario/login.html', form=form, title='Login')

@usuario.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    return redirect(url_for('usuario.login'))