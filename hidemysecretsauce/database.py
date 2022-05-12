import pymongo

client = pymongo.MongoClient()
db = client["sauce"]
users = db["users"]
sauces = db["sauces"]


def get_user_by_username(username):
    return users.find_one({'username': username})

def get_user_by_token(token):
    return users.find_one({'token': token})

def validate_password(username, password):
    user = get_user(username)
    # if user doesn't exist or password incorrect
    if user is None or not bcrypt.checkpw(password.encode('utf8'), user['password']):
        return False

    return True

def user_exists(username):
    return users.count_documents({'username': username}) != 0 

def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    users.insert_one({'username': username, 'password': hashed })

def add_refresh_token(username, token):
    users.update_one({'username': username}, { '$push': { 'token': str(token) } })
    return token





def add_sauce(username, sauce, ingredients):
    sauces.insert_one({'username': user['username'], 'name': sauce, 'ingredients': ingredients})

def delete_sauce(token, sauce_id):
    sauce = sauces.find_one({'_id': ObjectId(_id)})
    user = users.find_one({'token': token})
    if sauce['username'] != user['username']:
        raise ValueError

    sauces.delete_one({'_id': ObjectId(_id)})

def get_sauce_by_username(username):
    sauce_list = sauces.find({'username': user['username']})
    if sauce_list is None:
        sauce_list = []
    return sauce_list

