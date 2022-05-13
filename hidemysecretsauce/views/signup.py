from flask import Blueprint, request, render_template, redirect
from database import user_exists, add_user

signup = Blueprint('signup', __name__)

@signup.route('/signup', methods = ['GET', 'POST'])
def signup_method():
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

