from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASS = quote_plus(os.getenv("MONGO_PASS"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/test?retryWrites=true&w=majority"

def db_connection():
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    return client

@app.route("/books", methods=['GET', 'POST'])
def books():
    conn = db_connection()
    db = conn.get_database('books_database')
    collection = db.get_collection('books_collection')
    
    if request.method == 'GET':
        books = list(collection.find({}, {'_id': 0}))
        return jsonify(books)
    
    if request.method == 'POST':
        new_book = {
            "author": request.json.get("author"),
            "language": request.json.get("language"),
            "title": request.json.get("title")
        }
        collection.insert_one(new_book)
        return jsonify({"message": "Book added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
