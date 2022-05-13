import secrets
from flask import Blueprint, request, render_template, redirect
from database import *



login = Blueprint('login', __name__)
SECURE = False


@login.route('/login', methods = ['GET', 'POST'])
def login_method():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        # parse data from request
        username, password = request.form['username'], request.form['password']

        # if user doesn't exist or password incorrect
        if not user_exists(username) or not validate_password(username, password):
            return 'login error', 403

        token = secrets.token_bytes(20)
        add_refresh_token(username, token)
        response = redirect('/')

        if SECURE:
            response = redirect('/check_2fa')
        response.set_cookie('token', str(token))
        return response

@login.route('/logout', methods=['GET', 'POST'])
def logout_method():
    if request.method == 'GET':
        token = request.cookies.get('token', None)
        if token:
            response = redirect('/login')    
            response.set_cookie('token', '', expires=0)
            return response
        else:
            return 'user not logged in!'

