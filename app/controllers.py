from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

def user_registration(signup_form):
    hashed_password = generate_password_hash(signup_form.password.data)
    user = User(
        username=signup_form.username.data, 
        email = signup_form.email.data, 
        password_hash = hashed_password
        )
    db.session.add(user)
    db.session.commit()
    
    flash('Account created successfully! You can now log in.', 'success')

def verify_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None