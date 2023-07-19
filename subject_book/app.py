from flask import Flask, render_template, request, redirect, url_for, session
import db
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_EMAIL = 'admin@admin.com'
ADMIN_PASSWORD = 'morijyobi'

@app.route('/')
def index():
    books = db.select_all_books()
    return render_template('index.html', books=books)

@app.route('/search_books')
def search_books():
    query = request.args.get('query')
    books = db.search_books(query)
    if session.get('is_admin'):
        return render_template('a_login_success.html', books=books)
    elif 'user_id' in session:
        return render_template('login_success.html', books=books)
    else:
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

@app.route('/login_success')
def login_success():
    books = db.select_all_books()
    return render_template('login_success.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        
        if not title or not author or not isbn:
            return 'All fields are required'
        
        db.create_book(title, author, isbn)
        
        return redirect(url_for('a_login_success'))
    else:
        return render_template('add_book.html')

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    db.delete_book(book_id)
    return redirect(url_for('a_login_success'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        
        if not email or not password:
            return 'All fields are required'
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('a_login_success'))
        
        user = db.get_user_by_email(email)
        if not user:
            return 'Invalid email or password'
        
        salt = bytes.fromhex(user[5])
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        if hashed_password != user[4]:
            return 'Invalid email or password'
        
        session['user_id'] = user[0]
        
        return redirect(url_for('login_success'))
    else:
        return render_template('login.html')
    
@app.route('/a_login_success')
def a_login_success():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    books = db.select_all_books()
    return render_template('a_login_success.html', books=books)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        
        if not title or not author or not isbn:
            return 'All fields are required'
        
        db.update_book(book_id, title, author, isbn)
        
        return redirect(url_for('a_login_success'))
    else:
        book = db.select_book_by_id(book_id)
        return render_template('edit_book.html', book=book)

if __name__ == '__main__':
    app.run()