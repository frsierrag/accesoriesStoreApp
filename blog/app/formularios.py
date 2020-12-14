from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.core import FloatField, IntegerField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

class FormLogin(FlaskForm):
    userName = StringField('Usuario', validators=[DataRequired(message='Se requiere que completes este campo')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Se requiere que completes este campo')])
    remember = BooleanField('Recordar Usuario')
    submit = SubmitField('Iniciar Sesión')

class FormRecoverPass(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Este campo es requerido')])
    submit = SubmitField('Recuperar contraseña')

class FormChangePass(FlaskForm):
    newPassword = PasswordField('Nueva Contraseña', validators=[DataRequired(message='Se requiere que completes este campo')])
    confirmPassword = PasswordField('Confirmar Contraseña', validators=[DataRequired(message='Se requiere que completes este campo'), EqualTo('newPassword', message='Contraseña debe coincidir')])
    submit = SubmitField('Solicitar cambio de contraseña')

class FormRegister(FlaskForm):
    userName = StringField('Usuario', validators=[DataRequired(message='Se requiere que completes este campo')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Se requiere que completes este campo')])
    email = StringField('Email', validators=[DataRequired(message='Se requiere que completes este campo'), Length(min=5, max=35)])
    submit = SubmitField('+')

class FormCreate(FlaskForm):
    productName = StringField('Nombre', validators=[DataRequired(message='Se requiere que completes este campo'), Regexp('^-?[A-Za-z0-9áéíóúÁÉÍÓÚ ]*(\.[0-9]+)?$')])
    quantity = IntegerField('Capacidad', validators=[DataRequired(message='Se requiere que completes este campo'), Regexp('^-?[0-9]*(\.[0-9]+)?$')])
    price = FloatField('Precio', validators=[DataRequired(message='Se requiere que completes este campo'), Regexp('^-?[0-9]*(\.[0-9]+)?$')])
    image = FileField('File', validators=[DataRequired(message='Se requiere que completes este campo')])
    create = SubmitField('+')

class FormUpdate(FlaskForm): 
    productName = StringField('Nombre', validators=[DataRequired(message='Se requiere que completes este campo')])
    quantity = IntegerField('Capacidad', validators=[DataRequired(message='Se requiere que completes este campo')])
    price = FloatField('Precio', validators=[DataRequired(message='Se requiere que completes este campo')])
    image = FileField('File', validators=[DataRequired(message='Se requiere que completes este campo')])
    submit = SubmitField('Actualizar')

class FormDelete(FlaskForm):
    reference = StringField()
    submit = SubmitField('Eliminar')

class FormSearch(FlaskForm):
    product = StringField('Nombre', validators=[DataRequired(message='Se requiere que completes este campo')])
    search = SubmitField('Buscar')

class FormUpdateInventary(FlaskForm):
    quantity = IntegerField('Capacidad', validators=[DataRequired(message='Se requiere que completes este campo')])
    submit = SubmitField('Actualizar')