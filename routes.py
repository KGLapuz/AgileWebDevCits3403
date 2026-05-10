from flask import render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.log_in_page import app, db, RegistrationForm, LoginForm, User
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_in_page.html',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    signup_form = RegistrationForm()

    # for login post
    if login_form.submit_login.data and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password, login_form.password.data):
            session['user'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please Check email and password', 'error')
    
    # for signup post
    if signup_form.submit_signup.data and signup_form.validate_on_submit():
        hashed_password = generate_password_hash(signup_form.password.data)
        user = User(username=signup_form.username.data,
                    email = signup_form.emai.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    if signup_form.errors:
        flash('Please correct the errors in the sign up form.', 'error')
    
    return render_template('log_in_page.html', login_form=login_form, signup_form =signup_form)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"<h1>Success!</h1><p>Welcome to the dashboard, {session['user']}.</p><a href='/logout'>Logout</a>"
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower == 'true'
    app.run(debug=debug_mode)