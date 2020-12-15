import json
from app import app, bdd
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_manager, login_user, logout_user, login_required, current_user
from app.formularios import FormLogin, FormRecoverPass, FormChangePass, FormRegister, FormCreate, FormUpdate, FormDelete, FormSearch, FormUpdateInventary
from app.mocks import userValidate, listAccesories
from app.modelos import Usuario, Producto
from app.enviar_email import contraseña_olvidada
from werkzeug.urls import url_parse


UPLOAD_FOLDER = '/StoreApp/accesoriesStoreApp/blog/app/static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    #     user = userValidate(request.form["userName"], request.form["password"])
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if TipoUsuario:
            return redirect(url_for('home_admin'))
        else:
            return redirect(url_for('home_user'))
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.userName.data).first()
        administrador = Usuario.query.filter_by(username=form.userName.data).filter_by(admin=1).all()
        if usuario and not administrador:
            if usuario.verif_clave(form.password.data):
                login_user(usuario, remember=form.remember.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home_user')
                return redirect(next_page)
            else:
                form.password.errors.append("Contraseña incorrecta")
        elif usuario and administrador:
            if usuario.verif_clave(form.password.data):
                login_user(usuario, remember=form.remember.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home_admin')
                return redirect(next_page)
            else:
                form.password.errors.append("Contraseña incorrecta")
        else: form.userName.errors.append("Usuario incorrecto")
    return render_template('login.html', title='Iniciar Sesion', form=form)


@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if TipoUsuario:
            return redirect(url_for('home_admin'))
        else:
            return redirect(url_for('home_user'))
    form = FormRecoverPass()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        #usuarios = Usuario.query.all()
        if usuario is None:
            flash('No existe ningún usuario con este correo electrónico en nuestros registros')
            form.email.data = ""
            redirect(url_for('recover_password'))
        if usuario is not None:
            contraseña_olvidada(usuario)
            flash('Chequea tu email para completar la recuperación de contraseña')
            return redirect(url_for('login'))
    return render_template('recover_password.html', titulo='Recuperar contraseña', form=form)


@app.route('/change_pass/<token>', methods= ['GET', 'POST'])
def change_pass(token):
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if TipoUsuario:
            return redirect(url_for('home_admin'))
        else:
            return redirect(url_for('home_user'))
    usuario = Usuario.verificar_token_contraseña(token)
    if not usuario:
        return redirect(url_for('index'))
    form = FormChangePass()
    if form.validate_on_submit():
        usuario.def_clave(form.newPassword.data)
        bdd.session.commit()
        flash('Tu contraseña ha sido cambiada')
        return redirect(url_for('login'))
    return render_template('change_password.html', form=form)


@app.route('/home_admin')
@login_required
def home_admin():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if not TipoUsuario:
            return redirect(url_for('home_user'))        
    return render_template('/home_admin.html')


@app.route('/admin_register',methods=['GET','POST'])
@login_required
def admin_register():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if not TipoUsuario:
            return redirect(url_for('home_user'))
    form = FormRegister()
    if form.validate_on_submit():
        usuario = Usuario(username=form.userName.data, email=form.email.data, admin=False)
        usuario.def_clave(form.password.data)
        bdd.session.add(usuario)
        bdd.session.commit()
        flash('Usuario registrado correctamente')
        return redirect(url_for('home_admin'))
    return render_template('admin_register.html', form=form)


@app.route('/products_admin',methods=['GET','POST'])
@login_required
def products_admin():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if not TipoUsuario:
            return redirect(url_for('home_user'))
    formCreate = FormCreate()
    formSearch = FormSearch()
    if request.method == "GET":
        return render_template('/products_admin.html', stateSearch='', stateCreate='is-active', 
            formCreate=formCreate, formSearch=formSearch)
    else:
        if "searchProduct" in request.form:
            accesory = request.form["searchProduct"]
            lists = listAccesories(accesory)
            if lists != "1":
                return render_template('/products_admin.html', searchProducts=lists, stateSearch='is-active', 
                    stateCreate='', formCreate=formCreate)
            else:
                return render_template('/products_admin.html')
        elif "create" in request.form:
            file = request.files['file']
            # if file and allowed_file(file.filename):
            #     filename = secure_filename(file.filename)
            #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #     return redirect(url_for('uploaded_file', filename=filename))
            return render_template('/products_admin.html', formCreate=formCreate)
        return render_template('/products_admin.html', formCreate=formCreate, formSearch=formSearch, 
            stateSearch='', stateCreate='is-active',)


@app.route('/update_admin',methods=['GET','POST','DELETE'])
@login_required
def update_admin():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if not TipoUsuario:
            return redirect(url_for('home_user'))
    formUpdate = FormUpdate()
    formDelete = FormDelete()
    if request.method == "GET":
        product = request.args["accesory"]
        product = json.loads(product.replace("\'", "\""))
        if "accesory" in request.args:
            return render_template('/update_admin.html', formUpdate=formUpdate, searchProduct=product)
    elif request.method == "POST":
        if formUpdate.validate_on_submit():
            return render_template('/home_user.html')
        return render_template('/update_admin.html', formUpdate=formUpdate)
    elif request.method == "DELETE":
        return render_template('/update_admin.html', formDelete=formDelete)


@app.route('/home_user')
@login_required
def home_user():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if TipoUsuario:
            return redirect(url_for('home_admin'))        
    return render_template('/home_user.html')


@app.route('/products_user',methods=['GET','POST'])
@login_required
def products_user():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if TipoUsuario:
            return redirect(url_for('home_admin'))
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
@login_required
def update_user():
    if current_user.is_authenticated:
        TipoUsuario = current_user.admin
        if TipoUsuario:
            return redirect(url_for('home_admin'))
    formUpdateInventary = FormUpdateInventary()
    if request.method == "GET":
        product = request.args["accesory"]
        product = json.loads(product.replace("\'", "\""))
        if "accesory" in request.args:
            return render_template('/update_user.html', form=formUpdateInventary, searchProduct=product)
    else:
        if formUpdateInventary.validate_on_submit():
            return render_template('/home_user.html', form=formUpdateInventary)
        return render_template('/update_user.html', form=formUpdateInventary)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS