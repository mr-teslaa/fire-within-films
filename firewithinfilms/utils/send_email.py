#   importing necessary module
import os
import secrets
from flask import url_for
from flask import current_app
from flask_mail import Message
from firewithinfilms import mail


#   sending email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreplay@firewithinfilms.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
    <a href="{url_for('users.reset_token', token=token, _external=True)}">Reset Link</a>
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)