from flask import Flask, request, jsonify

app = Flask(__name__)

books_list = [
    {
        "bookid": 1,
        "author": "George Orwell",
        "language": "English",
        "title": "1984"
    },
    {
        "bookid": 2,
        "author": "Gabriel García Márquez",
        "language": "Spanish",
        "title": "One Hundred Years of Solitude"
    },
    {
        "bookid": 3,
        "author": "Haruki Murakami",
        "language": "Japanese",
        "title": "Norwegian Wood"
    },
    {
        "bookid": 4,
        "author": "Fyodor Dostoevsky",
        "language": "Russian",
        "title": "Crime and Punishment"
    },
    {
        "bookid": 5,
        "author": "J.K. Rowling",
        "language": "English",
        "title": "Harry Potter and the Sorcerer's Stone"
    }
]

@app.route('/books', methods =['GET','POST'])
def books():
    if request.method == 'GET':
        if len(books_list)>0:
            return jsonify(books_list)
        else:
            'No books found!'
    if request.method == 'POST':
        new_author = request.form['author']
        new_language = request.form['language']
        new_title = request.form['title']
        new_id = books_list[-1]['bookid'] + 1

        new_book = {
            'bookid': new_id,
            'author': new_author,
            'language': new_language,
            'title': new_title
        }

        books_list.append(new_book)
        return jsonify(books_list), 201

@app.route('/books/<int:bookid>', methods = ['GET', 'PUT', 'DELETE'])
def single_book(bookid):
    if request.method == 'GET':
        for book in books_list:
            if book['bookid'] == bookid:
                return jsonify(book)
        return 'Book not found', 404

    if request.method == 'PUT':
        for book in books_list:
            if book['bookid'] == bookid:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                updated_book = {
                    'bookid': bookid,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                return jsonify(updated_book)
        return 'Book not found', 404

    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['bookid'] == bookid:
                books_list.pop(index)
                return jsonify(books_list)
        return 'Book not found', 404
    
if __name__ == '__main__':
    app.run(debug=True)

