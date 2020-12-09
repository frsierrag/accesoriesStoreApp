from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.core import FloatField, IntegerField
from wtforms.fields.simple import FileField
from wtforms.validators import AnyOf, DataRequired

class FormInicio(FlaskForm):
    nombre = StringField('Usuario', validators=[DataRequired(message='Se requiere que completes este campo')])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message='Se requiere que completes este campo')])
    recordar = BooleanField('Recordar Usuario')
    enviar = SubmitField('Iniciar Sesión')

class FormRegister(FlaskForm):
    nombre = StringField('Usuario', validators=[DataRequired(message='Se requiere que completes este campo')])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message='Se requiere que completes este campo')])
    email = StringField('Email', validators=[DataRequired(message='Se requiere que completes este campo')])
    enviar = SubmitField('Iniciar Sesión')

class FormCreate(FlaskForm):
    referencia = ""  
    nombre = StringField('Nombre', validators=[DataRequired(message='Se requiere que completes este campo')])
    capacidad = IntegerField('Capacidad', validators=[DataRequired(message='Se requiere que completes este campo')])
    precio = FloatField('Precio', validators=[DataRequired(message='Se requiere que completes este campo')])
    imagen = FileField('File', validators=[DataRequired(message='Se requiere que completes este campo')])