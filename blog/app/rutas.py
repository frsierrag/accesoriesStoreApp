import os
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from app.formularios import FormLogin, FormRecover, FormRegister, FormCreate, FormUpdate, FormDelete, FormSearch, FormUpdateInventary
from app.mocks import userValidate, listAccesories
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = '/StoreApp/accesoriesStoreApp/blog/app/static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(user_id):
# 	return Usuarios.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = userValidate(request.form["userName"], request.form["password"])
        if user != "2":
            if user != "1":           
                # flash('Inicio de sesión solicitado por el usuario {}, recordar={}'.format(form.userName.data, form.remember.data))
                if user == "Admin":
                    return redirect(url_for('home_admin'))
                else:
                    return redirect(url_for('home_user'))
            else:
                form.password.errors.append("Contraseña incorrecta.")
        else:
            form.userName.errors.append("Usuario incorrecto.")
    return render_template('login.html', form=form)

@app.route('/recover_pass',methods=['GET','POST'])
def recover_password():
    form = FormRecover()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/home_admin')
def home_admin():
    return render_template('/home_admin.html')

@app.route('/admin_register',methods=['GET','POST'])
def admin_register():
    form = FormRegister()
    if form.validate_on_submit():
        return redirect(url_for('home_admin'))
    return render_template('admin_register.html', form=form)


@app.route('/products_admin',methods=['GET','POST'])
def products_admin():
    form_create = FormCreate()
    form_search = FormSearch()
    if request.method == "GET":
        return render_template('/products_admin.html', stateSearch='', stateCreate='is-active', 
            form_create=form_create, form_search=form_search)
    else:
        if "product" in request.form:
            accesory = request.form["product"]
            lists = listAccesories(accesory)
            print(lists)
            if lists != "1":
                return render_template('/products_admin.html', searchProducts=lists, stateSearch='is-active', 
                    stateCreate='', form_create=form_create, form_search=form_search)
            else:
                return render_template('/products_admin.html')
        elif "create" in request.form:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file', filename=filename))
            return render_template('/products_admin.html', form_create=form_create)
        return render_template('/products_admin.html', form_create=form_create, form_search=form_search, 
            stateSearch='', stateCreate='is-active',)


@app.route('/update_admin',methods=['GET','POST','DELETE'])
def update_admin():
    if request.method == "GET":
        form = FormUpdate()
        if form.validate_on_submit():
            return redirect(url_for('home_admin'))
        return render_template('/update_admin.html', form=form)
    elif request.method == "DELETE":
        form = FormDelete()
        if form.validate_on_submit():
            return redirect(url_for('home_admin'))
        return render_template('/update_admin.html', form=form)

@app.route('/home_user')
def home_user():
    return render_template('/home_user.html')

@app.route('/products_user',methods=['GET','POST'])
def products_user():
    if request.method == "GET":
        return render_template('/products_user.html')
    else:
        accesory = request.form["searchProduct"]
        lists = listAccesories(accesory)
        if lists != "1":
            return render_template('/products_user.html', searchProducts=lists)
        else:
            return render_template('/products_user.html')

@app.route('/update_user',methods=['GET','POST'])
def update_user():
    form = FormUpdateInventary()
    if form.validate_on_submit():
        return redirect(url_for('home_user'))
    return render_template('/update_user.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS