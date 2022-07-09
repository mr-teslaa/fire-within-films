from io import StringIO
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_login import current_user
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms import SelectField
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

    password = PasswordField(
        'Create New Password'
    )
    
    confirm_password = PasswordField(
        'Re-type New Password',
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


class UpdateAccountDescriptionForm(FlaskForm):
    description = TextAreaField(
        'Description',
        validators = [
            DataRequired()
        ]
    )

    primary_lang = SelectField(
        'Primary Language',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('hindi', 'Hindi' ),
            ('english', 'English' ),
            ('bangla', 'Bangla' ),
        ],
        validators = [
            DataRequired()
        ]
    )

    secondary_lang = SelectField(
        'Secondary Language',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('hindi', 'Hindi' ),
            ('english', 'English' ),
            ('bangla', 'Bangla' ),
        ],
        validators = [
            DataRequired()
        ]
    )

    skill_1 = SelectField(
        'Skill',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('singing', 'Singing' ),
            ('dancing', 'Dancing' ),
            ('voice artist', 'Voice Artist' ),
            ('acting', 'Acting' ),
            ('script writing', 'Script Writing' ),
        ],
        validators = [
            DataRequired()
        ]
    )

    skill_2 = SelectField(
        'Another Skill',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('singing', 'Singing' ),
            ('dancing', 'Dancing' ),
            ('voice artist', 'Voice Artist' ),
            ('acting', 'Acting' ),
            ('script writing', 'Script Writing' ),
        ],
    )

    skill_3 = SelectField(
        'Another Skill',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('singing', 'Singing' ),
            ('dancing', 'Dancing' ),
            ('voice artist', 'Voice Artist' ),
            ('acting', 'Acting' ),
            ('script writing', 'Script Writing' ),
        ],
    )

    skill_4 = SelectField(
        'Another Skill',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('singing', 'Singing' ),
            ('dancing', 'Dancing' ),
            ('voice artist', 'Voice Artist' ),
            ('acting', 'Acting' ),
            ('script writing', 'Script Writing' ),
        ],
    )

    skill_5 = SelectField(
        'Another Skill',
        choices = [
            ('N/A', '-- Select Class --' ),
            ('singing', 'Singing' ),
            ('dancing', 'Dancing' ),
            ('voice artist', 'Voice Artist' ),
            ('acting', 'Acting' ),
            ('script writing', 'Script Writing' ),
        ],
    )

    education_institue_name = StringField(
        'College/University Name',
    )

    education_graduation_name = StringField(
        'Course/Degree Name',
    )

    education_institue_country = StringField(
        'College/University Country',
    )

    education_graduation_year = StringField(
        'Graduated Year (Don\'t Fill up if your study is still running)'
    )

    submit = SubmitField('Update')


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