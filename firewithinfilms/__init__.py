from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from firewithinfilms.config import Config

from flask_admin import Admin
from firewithinfilms.admin import AccessAdminPanel

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin()
mail = Mail()

from firewithinfilms.models import User

#   define which route is mendatory if we try to access any unauthorize page.
#   in this case we are trying to access account page but before we access that page we must have to login first.
login_manager.login_view = 'users.user_login' # 'login' is the route name

#   beautify the flash message in login page which is authenticate by flask_login
login_manager.login_message_category = 'info' # 'info' is the bootstrap class name what will beautify our alert box

# config flask admin model view



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    admin = Admin(app, name='Fire Within Films', template_mode='bootstrap4')

    from firewithinfilms.models import User
    from firewithinfilms.models import UserPost
    from firewithinfilms.models import UserDetails
    from firewithinfilms.models import UserReviews

    from firewithinfilms.admin.views import adminview
    from firewithinfilms.user.views import user
    from firewithinfilms.public.views import public
    # from firewithinflims.main.routes import main
    app.register_blueprint(adminview)
    app.register_blueprint(user)
    app.register_blueprint(public)

    admin.add_view(AccessAdminPanel(User, db.session))
    admin.add_view(AccessAdminPanel(UserDetails, db.session))
    admin.add_view(AccessAdminPanel(UserReviews, db.session))
    admin.add_view(AccessAdminPanel(UserPost, db.session))

    return app
