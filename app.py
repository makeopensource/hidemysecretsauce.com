from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<p>Secret Sauces</p>'

@app.route('/login')
def login():
    pass

@app.route('/signup')
def signup():
    pass

@app.route('/setup_auth')
def setup_auth():
    pass



