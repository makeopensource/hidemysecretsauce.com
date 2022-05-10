import secrets
from flask import Flask, request, \
    render_template, url_for, redirect
from database import users
import bcrypt

app = Flask(__name__)

@app.route('/')
def home():
    token = request.cookies.get('token', None)
    if token:
        return 'Logged in'
    else:
        return redirect('/login')

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
        response = redirect('/')
        response.set_cookie('token', token)
        return response


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
        return redirect('/login') 

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return 'logged out'
    else:
        token = request.cookies.get('token', None)
        if token:
            response = redirect('/redirect')
            
            # doesn't successfully clear cookie
            response.set_cookie('token', '', expires=0)
            return response

