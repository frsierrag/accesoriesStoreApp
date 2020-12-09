from wtforms import StringField
from flask_wtf import FlaskForm
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.formularios import FormInicio, FormRegister, FormCreate
# from mocks import userValidate

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))
  

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = FormInicio()
    if(form.validate_on_submit()):
        # userValidate(form.nombre, form.contraseña)
        flash('Inicio de sesión solicitado por el usuario {}, recordar={}'.format(form.nombre.data, form.recordar.data))
        return redirect(url_for('home_admin'))
    return render_template('login.html', form=form)

@app.route('/admin_register',methods=['GET','POST'])
def admin_register():
    form = FormRegister()
    if(form.validate_on_submit()):
        return redirect(url_for('home_admin'))
    return render_template('admin_register.html', form=form)

@app.route('/home_admin')
def home_admin():
    return render_template('/home_admin.html')

@app.route('/home_user')
def home_user():
    return render_template('/home_user.html')

@app.route('/products_admin',methods=['GET','POST'])
def products_admin():
    form = FormCreate()
    if(form.validate_on_submit()):
        return redirect(url_for('home_admin'))
    return render_template('/products_admin.html')

@app.route('/products_user')
def products_user():
    return render_template('/products_user.html')

@app.route('/update_admin')
def update_admin():
    return render_template('/update_admin.html')

@app.route('/update_user')
def update_user():
    return render_template('/update_user.html')