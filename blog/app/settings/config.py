import os
class Ajustes(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'contraseña'
