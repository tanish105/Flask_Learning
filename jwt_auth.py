from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import jwt
import datetime
from functools import wraps

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Secret key for JWT
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASS = quote_plus(os.getenv("MONGO_PASS"))
MONGO_HOST = os.getenv("MONGO_HOST_2")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/test?retryWrites=true&w=majority"

def connect():
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    return client

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "token is missing!"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token is expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "token is invalid!"}), 401
        return f(*args, **kwargs)
    return decorated

def generate_token(username):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': expiration}, app.config['SECRET_KEY'], algorithm='HS256')
    return token
@app.route("/signup", methods=['POST'])
def signup():
    try:
        conn = connect()
        db = conn.get_database('users')
        collection = db.get_collection('signup')
        # Validate required fields
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        # Create new user
        new_user = {"username": username, "password": password}
        collection.insert_one(new_user)

        return jsonify({"message": "User added successfully!"}), 201

    except Exception as e:
        # Handle other potential errors gracefully
        return jsonify({"error": "An error occurred"}), 500

@app.route("/login", methods=['POST'])
def login():
    try:
        conn = connect()
        db = conn.get_database('users')
        collection = db.get_collection('signup')

        # Validate required fields
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        # Match the password with the username
        user = collection.find_one({"username": username, "password": password})
        if not user:
            return jsonify({"error": "Invalid username or password"}), 400

        # Generate JWT token
        token = generate_token(username)
        return jsonify({"message": "Login successful!", "token": token}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500

@app.route("/protected", methods=['GET'])
@token_required
def protected():
    return jsonify({"message": "This is a protected route"})

if __name__ == "__main__":
    app.run(debug=True)
