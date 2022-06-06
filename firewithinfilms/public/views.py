from flask import render_template
from flask import Blueprint

public = Blueprint('public', __name__)

#   LANDING PAGE
@public.route('/')
def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for('admindashboard'))
    return render_template('public/landing.html')

@public.route('/unauthorize')
def unauth():
    return "You are not authorize for this action"

