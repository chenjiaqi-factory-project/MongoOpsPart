import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('WEB_SERVER_SECRET_KEY') or 'abcdef020301abc8c86f'

    # MONGO_URI = "mongodb://dbuser:dbpassword@182.92.119.168:27017/testdb"
    MONGO_URI = os.environ.get('MONGO_URI')

    LOCALHOST_IP_PORT = '127.0.0.1:5000'
