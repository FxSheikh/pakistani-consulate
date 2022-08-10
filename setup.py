import os

SECRET_KEY = '\xaa\x8c\xa0\xfd\xd3\xa0C\xf08\xc0\x18\xe2\x80H\xaaQ\x93\t\x12\xc7\x91'
DEBUG=True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# database configuration settings
DB_USERNAME = ''
DB_PASSWORD = ''
DATABASE_NAME = ''
DB_HOST = ''
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI

# setting the maximum upload size to 1MB 
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

# '/flask_project/static/images' for the destinations

# configuring the upload set settings
UPLOADED_PHOTOS_DEST = 'static/documents/photos'
UPLOADED_PHOTOS_URL = 'static/documents/photos'

#/flask_project/ for destination

UPLOADED_LICENSES_DEST = 'static/documents/licenses'
UPLOADED_LICENSES_URL = 'static/documents/licenses'

UPLOADED_PASSPORTS_DEST = 'static/documents/passports'
UPLOADED_PASSPORTS_URL = 'static/documents/passports'

UPLOADED_NOCS_DEST = 'static/documents/nocs'
UPLOADED_NOCS_URL = 'static/documents/nocs'

UPLOADED_APPLIST_DEST = 'static/applists'
UPLOADED_APPLIST_URL = 'static/applists'

#EMAIL SETTINGS
MAIL_SERVER=''
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
