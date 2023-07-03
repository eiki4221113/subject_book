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
