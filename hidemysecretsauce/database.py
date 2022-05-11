import pymongo

client = pymongo.MongoClient()
db = client["sauce"]
users = db["users"]
sauces = db["sauces"]
