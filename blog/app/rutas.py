from wtforms import StringField
from flask_wtf import FlaskForm
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from app.formularios import FormLogin, FormRecover, FormRegister, FormCreate, FormUpdate, FormDelete, FormSearch, FormUpdateInventary

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = FormLogin()
    if(form.validate_on_submit()):
        flash('Inicio de sesión solicitado por el usuario {}, recordar={}'.format(form.nombre.data, form.recordar.data))
        return redirect(url_for('home_admin'))
    return render_template('login.html', form=form)

@app.route('/recover_pass',methods=['GET','POST'])
def recover_password():
    form = FormRecover()
    if(form.validate_on_submit()):
        return redirect(url_for('index'))
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

@app.route('/products_admin',methods=['GET','POST'])
def products_admin():
    form = FormCreate()
    if(form.validate_on_submit()):
        return redirect(url_for('home_admin'))
    return render_template('/products_admin.html', form=form)

@app.route('/update_admin',methods=['GET','POST','DELETE'])
def update_admin():
    if request.method == "POST":
        form = FormUpdate()
        if(form.validate_on_submit()):
            return redirect(url_for('home_admin'))
        return render_template('/update_admin.html', form=form)
    elif request.method == "DELETE":
        form = FormDelete()
        if(form.validate_on_submit()):
            return redirect(url_for('home_admin'))
        return render_template('/update_admin.html', form=form)

@app.route('/home_user',methods=['GET'])
def home_user():
    form = FormSearch()
    if(form.validate_on_submit()):
        return redirect(url_for('home_user'))
    return render_template('/home_user.html', form=form)

@app.route('/update_user',methods=['GET','POST'])
def update_user():
    form = FormUpdateInventary()
    if(form.validate_on_submit()):
        return redirect(url_for('home_user'))
    return render_template('/update_user.html', form=form)

@app.route('/products_user')
def products_user():
    return render_template('/products_user.html')