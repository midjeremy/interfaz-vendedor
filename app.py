from flask import Flask, render_template, redirect, url_for, request
from CRUD.crud import VerifiedPDF
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'jeremyampaimorales@gmail.com'
app.config['MAIL_PASSWORD'] = 'vyfh bzds ppfu umve'
app.config['MAIL_USE_TLS'] = True
#crear aplicacion mail
mail = Mail(app)

@app.route('/')
@app.route('/index')
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
            return redirect('/index')
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


if __name__ == '__main__':
    app.run(debug=True, port=5002)