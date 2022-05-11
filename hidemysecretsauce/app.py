import secrets
from flask import Flask, request, make_response, \
    render_template, url_for, redirect
from database import users, sauces
import bcrypt
import re
from bson.objectid import ObjectId




app = Flask(__name__)
SECURE = False



@app.route('/')
def home():
    token = request.cookies.get('token', None)
    if token:
        style = url_for('static', filename='css/style.css')
        js = url_for('static', filename='js/sauce.js')
        sauce_list = list(sauces.find())
        return render_template('sauces.html', style=style, js=js, sauces=sauce_list)
    else:
        return redirect('/signup')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        style = url_for('static', filename='css/style.css')
        return render_template(
            'form.html', 
            style=style, 
            form_title='Login',
            action='/login'
        )

    else:
        # parse data from request
        username, password = request.form['username'], request.form['password']
        return login_auth(username, password) 


# authenticate user given username and password
def login_auth(username, password):
    user = users.find_one({'name': username})

    # if user doesn't exist or password incorrect
    if user == None or not bcrypt.checkpw(password.encode('utf8'), user['password']):
        return 'login error', 403

    token = secrets.token_bytes(20)
    users.update_one({'name': username}, { '$push': { 'token': token } })
    response = redirect('/')
    response.set_cookie('token', token)
    return response


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        token = request.cookies.get('token', None)
        if token:
            response = redirect('/login')    
            response.set_cookie('token', '', expires=0)
            return response
        else:
            return 'user not logged in!'


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        style = url_for('static', filename='css/style.css')
        return render_template(
            'form.html', 
            style=style, 
            form_title='Sign In',
            action='/signup'
        )

    else:
        # parse data from request
        username, password = request.form['username'], request.form['password']
        if len(password) > 4:
            return 'Invalid Password'

        # check if user already exists
        if users.count_documents({'name': username}) != 0:
            return 'user exists'

        # insert new user
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert_one({'name': username, 'password': hashed })
        return login_auth(username, password)


@app.route('/add_sauce', methods=['POST'])
def add_sauce():
    sauce, ingredients = request.form['sauce'], request.form['ingredients']

    # check form integrity
    if sauce == '' or ingredients == '':
        return redirect('/')

    # clean input data
    sauce = sauce.title()
    ingredients = re.split('\s*,\s*', ingredients)
    ingredients = [x.title() for x in ingredients]

    # save sauce
    sauces.insert_one({'name': sauce, 'ingredients': ingredients})
    return redirect('/')

@app.route('/delete_sauce', methods=['POST'])
def delete_sauce():
    _id = request.json['_id']
    sauces.delete_one({'_id': ObjectId(_id)})
    return redirect('/')
