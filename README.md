# TIENDA DE ACCESORIOS - accesoriesStoreApp

# SUMMARY
App developed (in Python-Flask like back-edn and HTML, CSS and jQuery like front-end) to manage items in a catalog store, where it's possible creating, showing, updating and deleting accesories. Add this app has an user register system at the head of an Admin user.

# DESCRIPCIÓN
Aplicación desarrollada (en Python-Flask como back-end y HTML, CSS y jQuery para el front-end) para administrar elementos de una tienda por catalogo en la cual se pueden crear, mostrar, acatualizar y borrar accesorios. Adicionalmente la aplicación cuenta con un sistema de registro de usuarios a la cabeza de una cuenta de Administrador.

# SERVICIOS
1. Login: (GET/POST) Servicio de autenticación de usuario la cual compara la entrada con la información almacenada en base de datos.

2. Recuperación de contraseña: (GET/POST) Servicio de recuperación de contraseña para usuarios registrados por medio de el correo electrónico registrado.

3. Cambio de contraseña: (GET/POST) Servicio para recibir contraseña, confirmarla y actualizarla en la base de datos.

4. Registro de usuario: (GET/POST) Servicio para registro de usuarios con nombre, email y constraseña.

5. Creación de producto: (GET/POST) Servicio para crear producto con datos de entrada: Nombre de producto, cantidad, precio e imagen.

6. Actualización de producto: (GET/POST) Servicio para actualizar los productos en base de datos a través del ID generado por la base.

7. Eliminación de producto: (GET/POST/DELETE) Servicio para eliminar los productos en base de datos a través del ID generado por la base.

8. Búsqueda de producto: (GET/POST) Servicio para listar los productos relacionados con una entrada producida por el administrador o el usuario.

9. Actualización de inventarios: (GET/POST) Servicio para actualizar los inventarios de un producto en base de datos a través del ID generado por la base.

# DESCARGAS
Descarga este repositorio a través de: https://github.com/frsierrag/accesoriesStoreApp.git

# INSTALACIONES WINDOWS
pip install Flask
pip install Flask-wtf
pip install Flask-SQLAlchemy
pip install Flask-Migrate
pip install Flask-login
pip install Flask-JWT

# INSTALACIONES LINUX
sudo apt-get install python3-pip
sudo pip3 install flask
sudo pip3 install flask-wtf
sudo pip3 install flask-sqlalchemy
sudo pip3 install flask-migrate
sudo pip3 install flask-login
sudo pip3 install pyjwt

# EJECUCIÓN
Desde el ambiente de desarrollo sobre la carpeta \accesoriesStoreApp\blog ejecutar:
py blog.py 
https://localhost/index or
flask run 
http://localhost:5000/index

Desde el ambiente de producción sobre la carpeta ~/app/App/accesoriesStoreApp/blog$ ejecutar:
sudo python3 blog.py
https://ec2-3-91-199-11.compute-1.amazonaws.com/index

# INFO
frsierrag@gmail.com
fabiansierra@uninorte.edu.co
silviamm@uninorte.edu.co