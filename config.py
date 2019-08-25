import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('WEB_SERVER_SECRET_KEY') or 'abcdef020301abc8c86f'

    MONGO_URI = "mongodb://dbuser:dbpassword@45.78.76.192:27017/testdb"
