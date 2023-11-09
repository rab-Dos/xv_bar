from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort, copy_current_request_context
from waitress import serve
from flask.templating import render_template
from flask_mail import Mail, Message
from cryptography.fernet import Fernet 
import os
import configparser
import requests
import threading

#------------------------------------------------------------------Headers Server
project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'app/templates')
static_path = os.path.join(project_root, 'app/static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)
#------------------------------------------------------------------

#Función para limpiar consola
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#Clean Console
clearConsole()

#Correo
#Se carga archivo de configuración
config = configparser.ConfigParser()
config.read('./static/access/config.ini')

#acceso
fer = config['DEFAULT']['FER']
cypher = config['DEFAULT']['CYPHER']
fer = bytes(fer, 'utf-8')
cypher = bytes(cypher, 'utf-8')
siteKey = config['DEFAULT']['SITEKEY']
secretKey = config['DEFAULT']['SECRETKEY']
verifyURL = "https://www.google.com/recaptcha/api/siteverify"

#process
key = Fernet.generate_key()
f = Fernet(fer)
decypher = (f.decrypt(cypher)).decode()

def sendEmail(subject, name, email, phone, msg, to):
    message = Message(subject, sender = ('Consulta desde ortopediadrarreola.com', 'contacto@ortopediadrarreola.com'), recipients = [to])
    message.body = ".:: Recibimos la siguiente Consulta:\n\n-nombre: "+ name + "\n-correo: " + email + "\n-teléfono: " + phone + "\n-mensaje: " + msg
    mail.send(message)

def sendEmail2(subject2, name2, email2, phone2, msg2, to2):
    message2 = Message(subject2, sender = ('Dr. Atzin Arreola Ortopedista y Traumatólogo', 'contacto@ortopediadrarreola.com'), recipients = [to2])
    message2.body = ".:: Gracias por depositar su confianza en el Dr. Atzin Arreola\n\n:: Recibimos la siguiente Consulta:\n-nombre: "+ name2 + "\n-correo: " + email2 + "\n-teléfono: " + phone2 + "\n-mensaje: " + msg2 + "\n\n\nSu correo fue enviado correctamente, el Dr. se comunicara con usted en cuanto le sea posible.\n-= No es necesario responder este correo =-\n\n:: Calidad y Precisión en Cada Intervención ::"
    mail.send(message2)

#------------------------------------------------------------------Inicia aplicación

app = Flask(__name__)

#Control correo
app.config['MAIL_SERVER'] = 'mail.randrit.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'contacto@ortopediadrarreola.com'
app.config['MAIL_PASSWORD'] = decypher
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#Carpeta de archivos temporales
app.config['UFtemp'] = 'static/temp'

#Limite de memoria disponible para carga de archivos
app.config['MAX_CONTENT_LENGTH'] = 50000

#------------------------------------------------------------------Inicio de sesión

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html', siteKey=siteKey)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

#------------------------------------------------------------------Links a secciones controladas

def status_401(error):
    return redirect(url_for('home'))

def status_404(error):
    return redirect(url_for('home'))

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

#------------------------------------------------------------------Función Correo

@app.route('/sent', methods = ['GET', 'POST'])
def send():
    if request.method == 'POST':

        name = request.form['nombre']
        email = request.form['email']        
        msg = request.form['mensaje']

        if (name != "" and email != "" and msg != ""):

            secretResponse = request.form['g-recaptcha-response']
            verifyResponse = requests.post(url=f'{verifyURL}?secret={secretKey}&response={secretResponse}').json()

            if verifyResponse['success'] == False:
                abort(401)
            elif verifyResponse['score'] < 0.5:
                abort(401)
            else:
                # A correo de sitio
                subject = 'Correo enviado desde el Sitio Web'            
                phone = request.form['telefono']
                to = 'contacto@ortopediadrarreola.com'

                # A correo de usuario
                subject2 = 'Correo del Dr Atzin Arreola'
                name2 = name
                email2 = email
                phone2 = phone
                msg2 = msg
                to2 = email2

                @copy_current_request_context
                def sendMessage(subject, name, email, phone, msg, to):
                    sendEmail(subject, name, email, phone, msg, to)
                
                sender1 = threading.Thread(name='mail_sender', target=sendMessage, args=(subject, name, email, phone, msg, to))
                sender1.start()

                @copy_current_request_context
                def sendMessage2(subject2, name2, email2, phone2, msg2, to2):
                    sendEmail2(subject2, name2, email2, phone2, msg2, to2)
                
                sender2 = threading.Thread(name='mail_sender_2', target=sendMessage2, args=(subject2, name2, email2, phone2, msg2, to2))
                sender2.start()
        
        return ('', 204)        

@app.route('/mailok')
def mailok():    
    return render_template("mailok.html")

#------------------------------------------------------------------Inicia de ejecución
if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True, port=5500)
    # serve(app, host='localhost', port=5500, threads=30)
