import secrets
from flask import Flask, request, make_response, \
    render_template, url_for, redirect
from database import *
import bcrypt
import re
from bson.objectid import ObjectId
import qrcode
import pyotp


app = Flask(__name__)
SECURE = False


@app.route('/')
def home():
    token = request.cookies.get('token', None)
    if token:
        user = get_user_by_token(token)
        sauce_list = get_sauce_by_username(user['username']) 
        return render_template(
            'sauces.html',
            secure=SECURE,
            username=user['username'], 
            sauces=sauce_list
        )
    else:
        return redirect('/signup')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        # parse data from request
        username, password = request.form['username'], request.form['password']

        # if user doesn't exist or password incorrect
        if not user_exists(username):
            return 'login error', 403


        token = secrets.token_bytes(20)
        add_refresh_token(username, token)
        response = redirect('/')
        response.set_cookie('token', str(token))
        return response


@app.route('/check_2fa', methods=['GET', 'POST'])
def check_2fa():
    if request.method == 'GET':
        return render_template('/check_2fa.html')
    else:
        pass


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
        return render_template('signup.html')

    else:
        # parse data from request
        username, password = request.form['username'], request.form['password']
        if len(password) > 4:
            return 'Invalid Password'

        # check if user already exists
        if user_exists(username):
            return 'user exists'

        # insert new user
        add_user(username, password) 

        return redirect('/login')


@app.route('/setup_2fa', methods=['GET', 'POST'])
def setup_2fa():
    if request.method == 'GET' and 'token' in request.cookies:
        secret_key = pyotp.random_base32()
        user = get_user_by_token(request.cookies['token'])
        username = user['username']

        qr_code_data = pyotp.totp.TOTP(secret_key).provisioning_uri(
            name=username, 
            issuer_name='Hide My Secret Sauce'
        )

        qr_code = qrcode.make(qr_code_data)
        return render_template('setup_2fa.html', data=qr_code)

    else:
        # code, password = request.form['code'], request.form['password']
        return 'POST request to /setup_2fa'

@app.route('/add_sauce', methods=['POST'])
def add_sauce():
    token = request.cookies.get('token', None)
    if token:
        sauce, ingredients = request.form['sauce'], request.form['ingredients']

        # check form integrity
        if sauce == '' or ingredients == '':
            return redirect('/')

        # clean input data
        sauce = sauce.title()
        ingredients = re.split('\s*,\s*', ingredients)
        ingredients = [x.title() for x in ingredients]

        # save sauce
        user = get_user_by_token(token)
        add_sauce(user['username'], sauce, ingredients)
        return redirect('/')

    else:
        return 'Invalid request', 403

@app.route('/delete_sauce', methods=['POST'])
def delete_sauce():
    token = request.cookies.get('token', None)
    if token:
        _id = request.json['_id']
        try:
            delete_sauce(token, _id)
        except ValueError:
            return 'Invalid Request', 403
        return redirect('/')

    else:
        return 'Invalid Request', 403


if __name__ == '__main__':
    app.run()
