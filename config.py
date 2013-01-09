import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'SECRET_KEY_FOR_SESSION_SIGNING'


# Config Postgre - Heroku
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
DATABASE_CONNECT_OPTION = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'SOMETHING_IMPOSSIBLE_TO_GUEES'


#EMAIL SETTINGS
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'your_user@gmail.com'
MAIL_PASSWORD = 'your_password'

