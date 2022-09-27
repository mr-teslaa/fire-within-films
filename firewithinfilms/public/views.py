from flask import render_template
from flask import Blueprint

from firewithinfilms import mail
from flask_mail import Message

public = Blueprint('public', __name__)

#   LANDING PAGE
@public.route('/')
def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for('admindashboard'))
    return render_template('public/landing.html')

@public.route('/email')
def sendemail():
    msg = Message(
        "Hello",
        sender="sayhi@hossainfoysal.com",
        recipients=["mrnobody@labworld.org"]
    )
    msg.body = "another tesing email"
    mail.send(msg)
    return 'sending email'
    

@public.route('/unauthorize')
def unauth():
    return "You are not authorize for this action"

