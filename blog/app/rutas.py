import os, json
from app import app, bdd
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.formularios import FormLogin, FormRecoverPass, FormChangePass, FormRegister, FormCreate, FormUpdate, FormDelete, FormSearch, FormUpdateInventary
from app.mocks import listAccesories, createAccesories, updateAccesories, deleteAccesory
from app.modelos import Usuario, Producto
from app.enviar_email import contraseña_olvidada, envio_credenciales
from werkzeug.urls import url_parse


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
id_product = 0

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    # user = userValidate(request.form["userName"], request.form["password"])
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if tipoUsuario:
            return redirect(url_for('home_admin'))
        else:
            return redirect(url_for('home_user'))
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.userName.data).first()
        administrador = Usuario.query.filter_by(username=form.userName.data).filter_by(admin=1).all()
        if usuario and not administrador:
            # si es usuario ingresa esta condicion
            if usuario.verif_clave(form.password.data):
                login_user(usuario, remember=form.remember.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home_user')
                return redirect(next_page)
            else:
                form.password.errors.append("Contraseña incorrecta")
        elif usuario and administrador:
            # si es administrador ingresa esta condicion
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
        tipoUsuario = current_user.admin
        if tipoUsuario:
            return redirect(url_for('home_admin'))
        else:
            return redirect(url_for('home_user'))
    form = FormRecoverPass()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
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
        tipoUsuario = current_user.admin
        if tipoUsuario:
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
        tipoUsuario = current_user.admin
        if not tipoUsuario:
            return redirect(url_for('home_user'))        
    return render_template('/home_admin.html')


@app.route('/admin_register',methods=['GET','POST'])
@login_required
def admin_register():
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if not tipoUsuario:
            return redirect(url_for('home_user'))
    form = FormRegister()
    if form.validate_on_submit():
        usuario = Usuario(username=form.userName.data, email=form.email.data, admin=False)
        usuario.def_clave(form.password.data)
        bdd.session.add(usuario)
        bdd.session.commit()
        flash('Usuario registrado correctamente')
        envio_credenciales(form.userName.data, form.password.data, form.email.data)
        return redirect(url_for('home_admin'))
    return render_template('admin_register.html', form=form)


@app.route('/products_admin',methods=['GET','POST'])
@login_required
def products_admin():
    
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if not tipoUsuario:
            return redirect(url_for('home_user'))
    formCreate = FormCreate()
    formSearch = FormSearch()
    if request.method == "GET":
        return render_template('/products_admin.html', stateSearch='', stateCreate='is-active', 
            formCreate=formCreate, formSearch=formSearch)
    else:
        if "searchProduct" in request.form:
            accesory = request.form["searchProduct"]
            # lists = listAccesories(accesory)
            lists = Producto.query.filter(Producto.nombre.contains(accesory)).all()
            if len(lists) > 0:
                return render_template('/products_admin.html', searchProducts=lists, stateSearch='is-active', 
                    stateCreate='', formCreate=formCreate)
            else:
                lists = Producto.query.all()
                return render_template('/products_admin.html', searchProducts=lists, stateCreate='', 
                    stateSearch='is-active', formCreate=formCreate, formSearch=formSearch)
        if "image" in request.files:
            pic = request.files['image']
            while pic:
                if pic and allowed_file(pic.filename):
                    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
                    # createAccesories(formCreate)
                    accesory = Producto(nombre=formCreate.productName.data, precio=formCreate.price.data,
                        image="img/" + formCreate.image.data.filename, cantidad=formCreate.quantity.data
                        )
                    bdd.session.add(accesory)
                    bdd.session.commit()
                    return render_template('/home_admin.html')
                else: formCreate.image.errors.append('Extensión de imágen incorrecta')
        return render_template('/products_admin.html', formCreate=formCreate, formSearch=formSearch, 
            stateSearch='', stateCreate='is-active')


@app.route('/update_admin',methods=['GET','POST','DELETE'])
@login_required
def update_admin():
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if not tipoUsuario:
            return redirect(url_for('home_user'))
    formUpdate = FormUpdate()
    formDelete = FormDelete()
    if request.method == "GET":
        if "accesory" in request.args:
            product = request.args["accesory"]
            product = json.loads(product.replace("\'", "\""))
            return render_template('/update_admin.html', formUpdate=formUpdate, searchProduct=product)
        if "idProduct" in request.args:
            idProduct = request.args["idProduct"]
            # deleteAccesory(idProduct)
            bdd.session.query(Producto).filter(Producto.id==idProduct).delete(synchronize_session='evaluate')
            bdd.session.commit()
            return render_template('/home_admin.html')
    else:
        if "image" in request.files:
            pic = request.files['image']
            while pic:
                if pic and allowed_file(pic.filename):
                    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
                    # updateAccesories(formUpdate)
                    print(formUpdate.idReference)
                    print(formUpdate.productName.data)
                    bdd.session.query(Producto).filter(Producto.id==formUpdate.idReference.data).update(
                        {Producto.nombre:formUpdate.productName.data, Producto.image:"img/"+formUpdate.image.data.filename, 
                        Producto.cantidad:formUpdate.quantity.data}, synchronize_session='evaluate'
                    )
                    bdd.session.commit()
                    return render_template('/home_admin.html', formUpdate=formUpdate)
                else: formUpdate.image.errors.append('Extensión de imágen incorrecta')
        return render_template('/update_admin.html')


@app.route('/home_user')
@login_required
def home_user():
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if tipoUsuario:
            return redirect(url_for('home_admin'))        
    return render_template('/home_user.html')


@app.route('/products_user',methods=['GET','POST'])
@login_required
def products_user():
    global id_product
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if tipoUsuario:
            return redirect(url_for('home_admin'))
    if request.method == "GET":
        return render_template('/products_user.html')
    else:
        if "searchProduct" in request.form:
            accesory = request.form["searchProduct"]
            # lists = listAccesories(accesory)
            lists = Producto.query.filter(Producto.nombre.contains(accesory)).all()
            for i in lists:
                id_product = i.id
            
            if len(lists) > 0:
                return render_template('/products_user.html', searchProducts=lists)
            else:
                lists = Producto.query.all()
                return render_template('/products_user.html', searchProducts=lists)
            


@app.route('/update_user',methods=['GET','POST'])
@login_required
def update_user():
    global id_product
    print("id_product= ",id_product)
    if current_user.is_authenticated:
        tipoUsuario = current_user.admin
        if tipoUsuario:
            return redirect(url_for('home_admin'))
    form = FormUpdateInventary()
    if request.method == "GET":
        if "accesory" in request.args:
            product = request.args["accesory"]
            product = json.loads(product.replace("\'", "\""))
            return render_template('/update_user.html', formUpdateInventary=form, searchProduct=product)
        return render_template('/home_user.html')
    else:
        if "submit" in request.form:
            #bdd.session.query(Producto).filter(Producto.id==form.idReference.data).update(
            bdd.session.query(Producto).filter(Producto.id==id_product).update(
                {Producto.cantidad:form.quantity.data}, synchronize_session='evaluate'
            )
            bdd.session.commit()
        return render_template('/home_user.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html", error="Página no encontrada..."), 404


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


