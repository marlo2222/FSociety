from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)#alpha?
    email = db.Column(db.String(64), index=True, unique=True)
    is_prof = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(64))
    resumo = db.relationship('Resumo', backref='usuarios', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("A senha nao e um atributo que pode ser lido")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_professor(self):
        return self.is_prof

    def __repr__(self):
        return '<>Usuario: {}'.format(self.nome)

class Resumo(db.Model):
    __tablename__ = 'resumos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(64), unique=True)
    texto = db.Column(db.String(512))
    situacao = db.Column(db.String(32), default='Submetido')
    #autor = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    autores = db.relationship('Usuario', secondary=fk_usuarios_resumos, lazy='subquery',
    backref=db.backref('fk_resumos',lazy=True))

    def __repr__(self):
        return '<Resumo: {}>'.format(self.titulo)

class Avaliador(db.Model):
    __tablename__ = 'avaliadores'

    id = db.Column(db.Integer, primary_key=True)
    avaliador = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    resumo = db.Column(db.Integer, db.ForeignKey('resumos.id'))

    def __repr__(self):
        return '<>Avaliador: {}'.format(self.avaliador)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

fk_usuarios_resumos = db.Table('autores_do_resumo',
db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
db.Column('resumo_id', db.Integer, db.ForeignKey('resumos.id'), primary_key=True))

def informar_autores():
    pass