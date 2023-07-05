from flask import Flask, render_template, request, redirect, url_for, session
import db
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    books = db.select_all_books()
    return render_template('index.html', books=books)

@app.route('/search')
def search():
    query = request.args.get('query')
    books = db.search_books(query)
    return render_template('index.html', books=books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']   
        password = request.form['password']
        
        if not name or not phone_number or not email or not password:
            return 'All fields are required'
        
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        
        db.create_user(name, phone_number, email, hashed_password, salt.hex())
        
        return redirect(url_for('register_complete'))
    else:
        return render_template('register.html')

@app.route('/register_complete')
def register_complete():
    return render_template('register_complete.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            return 'All fields are required'
        
        user = db.get_user_by_email(email)
        if not user:
            return 'Invalid email or password'
        
        salt = bytes.fromhex(user[5])
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        if hashed_password != user[4]:
            return 'Invalid email or password'
        
        session['user_id'] = user[0]
        
        return render_template('login_success.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
