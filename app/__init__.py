import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import flask_wtf.csrf

from config import Config

csrf = flask_wtf.csrf.CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    with app.app_context():
        from . import models
        from .routes import main
        app.register_blueprint(main)
        return app