from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route('/')
def index():
    books = db.select_all_books()
    return render_template('index.html', books=books)


# @app.route('/list')
# def book_list():
#     books = db.select_all_books()
#     return render_template('index.html', books=books)

from flask import request

@app.route('/search')
def search():
    query = request.args.get('query')
    books = db.search_books(query)
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run()
