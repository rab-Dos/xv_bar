from flask import Flask, request, render_template, redirect, url_for, send_from_directory, send_file
from flask.templating import render_template
import pandas as pd
import random
import qrcode
from PIL import Image

#------------------------------------------------------------------Headers Server
# project_root = os.path.dirname(os.path.realpath('__file__'))
# template_path = os.path.join(project_root, 'app/templates')
# static_path = os.path.join(project_root, 'app/static')
# app = Flask(__name__, template_folder=template_path, static_folder=static_path)
#------------------------------------------------------------------

#------------------------------------------------------------------Inicia aplicación

app = Flask(__name__)

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
    return render_template('home.html')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

#Función para descarga
@app.route('/invitacion')
def invitacion(boleto):
    ruta = './static/boletaje/' + boleto
    resp = send_file(ruta, as_attachment=True)
    return resp

# Función Confirmar registro
@app.route('/boleto_ok')
def boleto_ok():
    return render_template("boleto_ok.html")

# Función para datos
@app.route('/send', methods = ['GET', 'POST'])
def send():
    if request.method == 'POST':

        name = request.form['nombre']
        phone = request.form['telefono']        
        invite = request.form['cantidad']
        total = int(invite) + 1
        folio = name[0:2].upper() + "-" + phone[-4:] + "-" + str(random.randint(0,9999))

        # Registro
        nuevorow = [name, phone, invite, total, folio]
        df = pd.read_csv('./static/db/invitados.csv')
        df = df.append(pd.DataFrame([nuevorow], columns=["nombre", "telefono", "invitados", "total", "folio"]), ignore_index=True)
        df.to_csv('./static/db/invitados.csv', index=False)

        # Generación de Boleto
        qrText = name + " viene con " + invite + " persona(s), en total son " + str(total) + " invitados. Tel:" + phone + " / Folio: " + folio
        img = qrcode.make(qrText)
        img = img.resize((150, 150))
        
        img_bg = Image.open('./static/img/invitacion_barb_png.png')
        img_bg.paste(img, (401, 0))
        boleto = 'Invitación_XC_Barbara_2023_' + folio + '.png'
        img_bg.save('./static/boletaje/'+boleto)
        
    return invitacion(boleto)

#------------------------------------------------------------------Links a secciones controladas

def status_401(error):
    return redirect(url_for('home'))

def status_404(error):
    return redirect(url_for('home'))

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

#------------------------------------------------------------------Inicia de ejecución
if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)
    # serve(app, host='localhost', port=5000, threads=30)