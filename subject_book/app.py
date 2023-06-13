from flask import Flask, render_template,request

import random
import db


app = Flask(__name__)

# レイアウトサンプル
@app.route('/')
def sample_top():
    return render_template('index.html')

@app.route('/list')
def sample_list():
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)

@app.route('/register')
def sample_register():
    return render_template('register.html')

@app.route('/search')
def sample_search():
    return render_template('search.html')

@app.route('/register_exe', methods={'POST'})
def register_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')
    
    db.insert_book(title, author, publisher, pages)

    book_list=db.select_all_books()

    return render_template('list.html', books=book_list)

    
if __name__ == '__main__':
    app.run(debug=True)