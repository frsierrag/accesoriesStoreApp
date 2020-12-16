from app.settings.config import ConexionMail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template
from app import app
from threading import Thread


def email_asincrono(server, mensaje):
    server.sendmail(mensaje['From'], mensaje['To'], mensaje.as_string())
    server.quit()


def contraseña_olvidada(usuario):
    # Configurando servidor email para contraseñas olvidadas
    #print("holaaaaa ", usuario.email)
    mensaje = MIMEMultipart() # Creamos el objeto mensaje
    token = usuario.obtener_token_contraseña()
    password = ConexionMail.MAIL_PASSWORD
    msj = render_template('mail_recover.txt', usuario=usuario, token=token)
    mensaje['From'] = ConexionMail.MAIL_USERNAME
    mensaje['To'] = usuario.email
    mensaje['Subject'] = 'Recuperar contraseña'
    mensaje.attach(MIMEText(msj, 'plain')) # Le decimos que el mensaje contiene solamente texto plano
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(mensaje['From'], password)
    Thread(target=email_asincrono, args=(server,mensaje)).start()


def envio_credenciales(nameUser, passwordUser, emailUser):
    # Configurando servidor email 
    mensaje = MIMEMultipart() # Creamos el objeto mensaje
    msj = 'Hola, se ha registrado correctamente en el sistema de Inventario. Su usuario es: ' + nameUser + ' y su contraseña es: ' +  passwordUser + '. Atentamente Soporte Inventario'
    password = ConexionMail.MAIL_PASSWORD
    mensaje['From'] = ConexionMail.MAIL_USERNAME
    mensaje['To'] = emailUser
    mensaje['Subject'] = 'Credenciales para ingreso a Inventario'
    mensaje.attach(MIMEText(msj, 'plain')) # Le decimos que el mensaje contiene solamente texto plano
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(mensaje['From'], password)
    server.sendmail(mensaje['From'], mensaje['To'], mensaje.as_string())
    server.quit()