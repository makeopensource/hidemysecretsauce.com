from flask import Blueprint, request, redirect
from database import add_sauce, get_user_by_token, delete_sauce
import re


sauce = Blueprint('sauce', __name__)
SECURE = False

@sauce.route('/add_sauce', methods=['POST'])
def add_sauce_route():
    token = request.cookies.get('token', None)
    if token:
        sauce, ingredients = request.form['sauce'], request.form['ingredients']

        # check form integrity
        if sauce == '' or ingredients == '':
            return redirect('/')

        # clean input data
        sauce = sauce.title()
        ingredients = re.split(r'\s*,\s*', ingredients)
        ingredients = [x.title() for x in ingredients]

        # save sauce
        user = get_user_by_token(token)
        add_sauce(user['username'], sauce, ingredients)
        return redirect('/')

    else:
        return 'Invalid request', 403

@sauce.route('/delete_sauce', methods=['POST'])
def delete_sauce_route():
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

