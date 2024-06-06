from flask import Flask, request, jsonify
import sqlite3 

app = Flask(__name__)

# create_table = """
# CREATE TABLE IF NOT EXISTS books (
#     id INTEGER PRIMARY KEY,
#     author TEXT NOT NULL,
#     language TEXT NOT NULL,
#     title TEXT NOT NULL
# )
# """

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route('/books', methods =['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute('select * from books')
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
        
    if request.method == 'POST':
        new_author = request.form['author']
        new_language = request.form['language']
        new_title = request.form['title']
        add_query = 'insert into books (author,language,title) values (?,?,?) '
        cursor.execute(add_query, (new_author, new_language, new_title))
        conn.commit()
        return 'Book with the id: {cursor.lastrowid} created successfully', 201

@app.route('/books/<int:bookid>', methods = ['GET', 'PUT', 'DELETE'])
def single_book(bookid):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute('select * from books where id=?', (bookid,))
        book = cursor.fetchone()
        if book is not None:
            return jsonify({'id': book[0], 'author': book[1], 'language': book[2], 'title': book[3]})
        else:
            return 'Book not found', 404

    if request.method == 'PUT':
        update_query ="""
        UPDATE books set author = ?, language = ?, title = ? where id = ?
"""
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        cursor.execute(update_query, (author, language, title, bookid))
        conn.commit()
        cursor.execute('select * from books where id=?', (bookid,))
        book = cursor.fetchone()
        if book is not None:
            return jsonify({'id': book[0], 'author': book[1], 'language': book[2], 'title': book[3]})
        else:
            return "book not updated", 404

    if request.method == 'DELETE':
        delete_query = """
        Delete from books where id = ?"""
        cursor.execute(delete_query, (bookid,))
        conn.commit()
        return 'Book deleted', 204

if __name__ == '__main__':
    app.run(debug=True)
