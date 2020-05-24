from flask import Flask, request, make_response, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mzeriorwuese@gmail.com'
app.config['MAIL_PASSWORD'] = 'xvtusfllhozhmeva'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Hello. This is my first flask message', sender = 'mzeriorwuese@gmail.com', recipients = ['mzermichael4@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True, host='127.0.0.1')
