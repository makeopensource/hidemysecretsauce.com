from flask import Blueprint, request, render_template, redirect
from database import *


homepage = Blueprint('homepage', __name__)
SECURE = False


@homepage.route('/')
def home():
    token = request.cookies.get('token', None)
    if token and get_user_by_token(token):
        user = get_user_by_token(token)
        sauce_list = get_sauce_by_username(user['username']) 
        return render_template(
            'sauces.html',
            secure=SECURE,
            username=user['username'], 
            sauces=sauce_list
        )
    else:
        response = redirect('/signup')
        response.set_cookie('token', '', expires=0)
        return response

