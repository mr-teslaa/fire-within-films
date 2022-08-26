from datetime import datetime
from email.policy import default
from signal import default_int_handler
from firewithinfilms import db
from firewithinfilms import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#   all kind of user with multiple role
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_role = db.Column(db.String(60), default="user")
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.relationship('UserDetails', backref='details', lazy=True)
    reviews = db.relationship('UserReviews', backref='reviews', lazy=True)
    posts = db.relationship('UserPost', backref='author', lazy=True)

#   post table for all
class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    user_headline = db.Column(db.String(100), default="Your Headline")
    country = db.Column(db.String(100), default='India')
    description = db.Column(db.Text, nullable=False, default="Write about yourself")
    primary_lang = db.Column(db.String(100), default='N/A')
    secondary_lang = db.Column(db.String(100), default='N/A')
    skill_1 = db.Column(db.String(100), default='N/A')
    skill_2 = db.Column(db.String(100), default='N/A')
    skill_3 = db.Column(db.String(100), default='N/A')
    skill_4 = db.Column(db.String(100), default='N/A')
    skill_5 = db.Column(db.String(100), default='N/A')
    education_institue_name = db.Column(db.String(300), default='N/A')
    education_graduation_name = db.Column(db.String(300), default='N/A')
    education_institue_country = db.Column(db.String(100), default='N/A')
    education_graduation_year = db.Column(db.String(100), default="0")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#   post table for all
class UserReviews(db.Model):
    __tablename__ = 'user_reviews'
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.String(100), default='0')
    date_given = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avg_star = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#   post table for all
class UserPost(db.Model):
    __tablename__ = 'user_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)