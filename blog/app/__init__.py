from flask import Flask, render_template, redirect, url_for
from app.settings.config import Ajustes, ConexionMail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Ajustes)
bdd = SQLAlchemy(app)
migrar = Migrate(app,bdd)
login = LoginManager(app)
login.login_view = 'login'

login.login_message = 'Por favor inicia sesión para acceder a esta página.'

from app import rutas, modelos


