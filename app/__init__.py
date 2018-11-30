from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.login_view = 'usuario.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .usuario import usuario as usuario_blueprint
    app.register_blueprint(usuario_blueprint)

    from .aluno import aluno as aluno_blueprint
    app.register_blueprint(aluno_blueprint)

    from .professor import professor as professor_blueprint
    app.register_blueprint(professor_blueprint)

    return app