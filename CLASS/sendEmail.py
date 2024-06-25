from flask_mail import Mail, Message
from flask import Flask, render_template

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'jeremyampaimorales@gmail.com'
app.config['MAIL_PASSWORD'] = 'vyfh bzds ppfu umve'
app.config['MAIL_USE_TLS'] = True
#crear aplicacion mail
mail = Mail(app)

class SendEmail:
    def __init__(self, email, oferta, template):
        self.email = email
        self.oferta = oferta
        self.template = template


        destinario = self.email

        msg = Message('Ofertas', sender='noreply@masterbikes.com', recipients=[destinario])
        data = {
            'ofertas': self.oferta
        }
        msg.html = render_template(self.template, data=data)
        
        return mail.send(msg)