from flask import Flask, render_template, redirect, url_for, request
from CRUD.crud import VerifiedPDF, agregarProductos, VerifiedIMG, buscarIMG
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from CONEX.Conex import conexion
from CLASS.CreatePDF import CreatePDF
import base64


rutaPDF = './TEMPLATES/'

conex = conexion()

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'jeremyampaimorales@gmail.com'
app.config['MAIL_PASSWORD'] = 'vyfh bzds ppfu umve'
app.config['MAIL_USE_TLS'] = True
#crear aplicacion mail
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-PDF', methods = ['GET', 'POST'])
def submitPDF():

    if request.method == 'POST':
        archivo = request.files['archivoPDF']
        codigoTrabajador = request.form['codigoTrabajador']
        email = request.form['email']

        
        if archivo and VerifiedPDF(archivo.filename):
            filename= secure_filename(archivo.filename)

            msg = Message('Reportes de informe de problemas/Soluciones', sender='noreply@masterbikes.com', recipients=[email])
            msg.attach(filename, 'application/pdf', archivo.read())
            mail.send(msg)
            return redirect('/')
        elif archivo.filename == '':
            error = 'No se encuentra ningun formato PDF'
            return render_template('enviarPDF.html', error = error)
        else:
            error = '''Ese archivo no es un PDF.
            Favor envie un archivo PDF'''
            return render_template('enviarPDF.html', error = error)
    return render_template('enviarPDF.html')

@app.route('/buscar-boleta')
def buscarBoleta():
    return render_template('buscarBoleta.html')


@app.route('/crear-PDF', methods = ['GET'])
def crearPDF():
    if request.method == 'GET':
        CreatePDF(rutaPDF)
        return redirect('/')

@app.route('/agregar-producto', methods=['GET', 'POST'])
def agregrarProducto():
    if request.method == 'POST':
        nombre = request.form['producto']
        descripcion = request.form['Des-producto']
        precio = request.form['precio']
        stock = request.form['stock']
        imagen = request.files['producto-img']
        
        if imagen and VerifiedIMG(imagen.filename):
            filename = secure_filename(imagen.filename)
            img = imagen.read()
            agregarProductos(nombre,descripcion,precio,stock,img)
            return redirect('/')
        elif imagen == '':
            error = 'Debes mandar alguna imagen'
            return render_template('agregarProducto.html', error = error)
        else:
            error = 'Solo se puede mandar imagenes tipo png, jpg, webp'
            return render_template('agregarProducto.html', error = error)

    return render_template('agregarProducto.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)