import pymongo
import hashlib
from bson.objectid import ObjectId

client = pymongo.MongoClient()
db = client["sauce"]
users = db["users"]
sauces = db["sauces"]


def get_user_by_username(username):
    return users.find_one({'username': username})

def get_user_by_token(token):
    return users.find_one({'token': token})

def validate_password(username, password):
    user = get_user_by_username(username)
    # if user doesn't exist or password incorrect
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return user is not None and hashed == user['password']

def user_exists(username):
    return users.count_documents({'username': username}) != 0 

def add_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    users.insert_one({'username': username, 'password': hashed })

def add_refresh_token(username, token):
    users.update_one({'username': username}, { '$push': { 'token': str(token) } })
    return token

def store_secret_key(username, secret_key):
    users.update_one({'username': username}, { '$set': { 'secret_key': secret_key } })



def add_sauce(username, sauce, ingredients):
    sauces.insert_one({'username': username, 'name': sauce, 'ingredients': ingredients})

def delete_sauce(token, sauce_id):
    sauce = sauces.find_one({'_id': ObjectId(sauce_id)})
    user = users.find_one({'token': token})
    if sauce['username'] != user['username']:
        raise ValueError

    sauces.delete_one({'_id': ObjectId(sauce_id)})

def get_sauce_by_username(username):
    sauce_list = sauces.find({'username': username})
    if sauce_list is None:
        sauce_list = []
    return sauce_list

