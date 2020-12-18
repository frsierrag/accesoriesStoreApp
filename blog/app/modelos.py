import jwt
from app import bdd, login
from time import time
from app import app
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
from flask_login import UserMixin


association_table = bdd.Table(
    'association', bdd.Model.metadata,
    bdd.Column('users_id', bdd.Integer, bdd.ForeignKey(
        'users.id'), primary_key=True),
    bdd.Column('products_id', bdd.Integer, bdd.ForeignKey(
        'products.id'), primary_key=True))


class Usuario(UserMixin, bdd.Model):
    __tablename__ = 'users'
    id = bdd.Column(bdd.Integer, primary_key=True)
    username = bdd.Column(bdd.String(64), index=True, unique=True)
    email = bdd.Column(bdd.String(120), index=True, unique=True)
    hash_clave = bdd.Column(bdd.String(128))
    admin = bdd.Column(bdd.Boolean, default=False)
    productos = bdd.relationship(
        'Producto',
        secondary=association_table,
        backref=bdd.backref('usuarios', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<Usuario {}>'.format(self.username)        

    def def_clave(self, clave):
        self.hash_clave = genph(clave)

    def verif_clave(self, clave):
        return checkph(self.hash_clave, clave)

    def obtener_token_contraseña(self, expiracion=600):
        return jwt.encode(
            {'recuperar_contraseña': self.id, 'expide': time() + expiracion},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verificar_token_contraseña(token):
        try:
            id = jwt.decode(
                token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['recuperar_contraseña']
        except:
            return
        return Usuario.query.get(id)


class Producto(bdd.Model):
    __tablename__ = 'products'
    id = bdd.Column(bdd.Integer, primary_key=True)
    nombre = bdd.Column(bdd.String(100), nullable=False)
    precio = bdd.Column(bdd.Float, default=0)
    image = bdd.Column(bdd.String(255))
    cantidad = bdd.Column(bdd.Integer, default=0)

    def precio_final(self):
        return self.precio+(self.precio)

    def __repr__(self):
        product = {'id':self.id, 'name':self.nombre, 'price':self.precio, 'image':self.image, 'quantity':self.cantidad}
        return f"{product}"

    # def __repr__(self):
    #     return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


@login.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))
