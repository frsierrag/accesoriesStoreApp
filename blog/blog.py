from app import app, bdd
from app.modelos import Usuario, Producto

@app.shell_context_processor
def make_shell_context():
  return {'bdd':bdd, 'Usuario':Usuario, 'Producto':Producto}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem') )
