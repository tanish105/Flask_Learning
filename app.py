from flask import Flask, request, session

app = Flask(__name__)

# Set a secret key for sessions
app.secret_key = 'supersecretkey'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/<name>')
def show_name(name):
    return f"Hello, {name}"

@app.route('/set/<value>')
def set_session(value):
    session['key'] = value
    return f'Session value set to {value}'

@app.route('/get')
def get_session():
    value = session.get('key', 'Not set')
    return f'Session value is {value}'

@app.route('/request_info')
def request_info():
    user_agent = request.headers.get('User-Agent')
    return f'Your user agent is {user_agent}'

if __name__ == '__main__':
    app.run(debug=True)
