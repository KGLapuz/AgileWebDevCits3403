import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_DIR = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DATA_DIR)
    SECRET_KEY = "bronte-keithlin-mambwe" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False