import os


class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/firewithinflims'
    # set optional bootswatch theme
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'premium249.web-hosting.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'sayhi@hossainfoysal.com'        # os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = 'hossainfoysal.emailaddress.sayhi'        # os.environ.get('EMAIL_PASSWORD')