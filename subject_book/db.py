import os
import psycopg2

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = " select * from subject_books"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows
def search_books(query):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM subject_books WHERE title LIKE %s OR author LIKE %s"
    cursor.execute(sql, ('%' + query + '%', '%' + query + '%'))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def create_user(name, phone_number, email, hashed_password, salt):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO subject_user (name, phone_number, email, hashed_password, salt) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, phone_number, email, hashed_password, salt))
    connection.commit()
    cursor.close()
    connection.close()

def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM subject_user WHERE email = %s"
    cursor.execute(sql, (email,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row

def create_book(title, author, isbn):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO subject_books (title, author, isbn) VALUES (%s, %s, %s)"
    cursor.execute(sql, (title, author, isbn))
    connection.commit()
    cursor.close()
    connection.close()
    
def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM subject_books WHERE id = %s"
    cursor.execute(sql, (book_id,))
    # 図書を消去したあとに新たに図書を登録するとidがずれるためidのリセット機能を追加（errorが出た場合消去）
    cursor.execute("SELECT setval('subject_books_id_seq', (SELECT MAX(id) FROM subject_books))")
    connection.commit()
    cursor.close()
    connection.close()
