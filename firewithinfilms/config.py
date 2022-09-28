import os
from dotenv import find_dotenv
from dotenv import load_dotenv

load_dotenv(find_dotenv())

production=True
# production=False

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'

    if production:
        SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/firewithinflims'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
        
    # set optional bootswatch theme
    FLASK_ADMIN_SWATCH = 'cerulean'

    #   SETUP SMTP MAIL SERVER
    MAIL_SERVER = os.getenv('EMAIL_SMTP_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL_USERNAME')        
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')