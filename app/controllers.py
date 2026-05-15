from . import db
from .models import User
from flask import flash

def user_registration(signup_form):
    user = User(
        username=signup_form.username.data, 
        email = signup_form.email.data
        )
    
    user.password_hash = signup_form.password.data
    
    db.session.add(user)
    db.session.commit()
    
    flash('Account created successfully! You can now log in.', 'success')

def verify_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.authenticate(password):
        return user
    return None