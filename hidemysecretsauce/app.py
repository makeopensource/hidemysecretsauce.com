import secrets
from flask import Flask, make_response, request, \
    render_template, url_for
from database import users
import bcrypt

app = Flask(__name__)

@app.route('/')
def home():
    static_file = url_for('static', filename='css/style.css')
    return render_template('login.html', static_file = static_file)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        static_file = url_for('static', filename='css/style.css')
        return render_template('login.html', static_file = static_file)

    else:
        print(request.form)
        # parse data from request
        username, password = request.form['username'], request.form['password']

        user = users.find_one({'name': username})

        # if user doesn't exist or password incorrect
        if user == None or not bcrypt.checkpw(password.encode('utf8'), user['password']):
            return 'login error', 403

        token = secrets.token_bytes(20)
        users.update_one({'name': username}, { '$push': { 'token': token } })
        resp = make_response('success')
        resp.set_cookie('token', token)
        return resp


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        static_file = url_for('static', filename='css/style.css')
        return render_template('signup.html', static_file = static_file)

    else:
        # parse data from request
        username, password = request.form['username'], request.form['password']

        # check if user already exists
        if users.count_documents({'name': username}) != 0:
            return 'user exists', 409

        # insert new user
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert_one({'name': username, 'password': hashed })
        return 'success', 200

@app.route('/setup_auth')
def setup_auth():
    pass



