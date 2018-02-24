import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@192.168.56.101:3306/example'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False