from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_login import current_user
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from firewithinfilms.models import User


class RegistrationForm(FlaskForm):
    
    username = StringField(
        'Username',
        validators = [
            DataRequired(), 
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators = [
            DataRequired(), 
            Email()
        ]
    )

    password = PasswordField(
        'Password', 
        validators = [ 
            DataRequired()
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(), 
            EqualTo('password')
        ]
    )
    
    submit = SubmitField('Create account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [
            DataRequired(), 
            Email()
        ]
    )

    password = PasswordField(
        'Password', 
        validators = [DataRequired()]
    )

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    name = StringField(
        'Name',
        validators = [ 
            Length(min=2, max=50)
        ]
    )

    username = StringField(
        'Username',
        validators = [ 
            Length(min=2, max=20)
        ]
    )

    profile_title = StringField(
        'Profile Title',
        validators = [ 
            Length(min=5, max=50)
        ]
    )

    country = StringField(
        'Country'
    )

    email = StringField(
        'Email',
        validators = [
            Email()
        ]
    )

    picture = FileField(
        'Update Profile Picture', 
        validators = [
            FileAllowed(['jpg','jpeg','png'])
        ]
    )

    profile_description = StringField(
        'Profile Description',
        validators = [
            Length(min=50, max=500)
        ]
    )

    primary_lang = StringField(
        'Primary Laguage'
    )

    secondery_lang = StringField(
        'Secondary Laguage'
    )

    password = PasswordField(
        'Password'
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            EqualTo('password')
        ]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('What is happening?', validators=[DataRequired()])
    picture = FileField(
        'Add a banner image', 
        validators = [
            FileAllowed(['jpg', 'jpeg', 'png'])
        ]
    )
    submit = SubmitField('Post')