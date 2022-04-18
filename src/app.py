from crypt import methods
import secrets
from flask import Flask, make_response, request
from database import users
import bcrypt

app = Flask(__name__)

@app.route('/')
def home():
    return '<p>Secret Sauces</p>'

@app.route('/login')
def login():
    # parse data from request
    username, password = request.form['username'], request.form['password']

    user = users.find_one({'name': username})
    if bcrypt.checkpw(password, user.password):
        token = secrets.token_bytes(20)
        user['token'] = user.get('token', []).append(token)
        users.replace_one({'name': username}, user)
        resp = make_response("success")
        resp.set_cookie("token", token)
        return resp
    
    # not correct login
    return "login error", 403
    

@app.route('/signup', methods = ["POST"])
def signup():
    # parse data from request
    username, password = request.form['username'], request.form['password']

    # check if user already exists
    if users.count_documents({'name': username}) != 0:
        return "user exists", 409

    # insert new user
    users.insert_one({'name': username, 'password': bcrypt.hashpw(password, bcrypt.gensalt())})
    return "success", 200

@app.route('/setup_auth')
def setup_auth():
    pass



