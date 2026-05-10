from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z](?=.\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$)',
               message="Password must be 8+ chars, have 1 uppercase, 1 lowercase, 1 number, and 1 special char.")
    ])
    submit_signup = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            ValidationError('Email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_login = SubmitField('Sign in')