import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_DIR = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DB_DIR)
    SECRET_KEY = "bronte-keithlin-mambwe" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False