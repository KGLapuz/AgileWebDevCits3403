import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_DIR = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SECRET_KEY = "bronte-keithlin-mambwe" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DB_DIR)
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False