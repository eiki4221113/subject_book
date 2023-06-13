import os
import psycopg2

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title, author, publisher, pages FROM books_sample"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def insert_book(title, autohor, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO books_sample VALUES (default ,%s, %s, %s, %s)"
    
    cursor.execute(sql, (title, autohor, publisher, pages))
    connection.commit()
    
    cursor.close()
    connection.close()