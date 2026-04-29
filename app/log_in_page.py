from flask import Flask, session, redirect, \
url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'mysecret'

TEST_DATA = {
    "admin": "password123",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_in_page.html',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in TEST_DATA and TEST_DATA[email] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            error = "Incorrect username or password. Please try again."

    return render_template('log_in_page.html' , error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"<h1>Success!</h1><p>Welcome to the dashboard, {session['user']}.</p><a href='/logout'>Logout</a>"
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)