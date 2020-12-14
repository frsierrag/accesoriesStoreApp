import os
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class Ajustes(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'contraseña'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ConexionMail(object):
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'soporte.inventariouninorte@gmail.com'
    MAIL_PASSWORD = 'soporte1234'
    ADMINS = 'soporte.inventariouninorte@gmail.com'
