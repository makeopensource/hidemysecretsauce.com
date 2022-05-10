import pymongo

client = pymongo.MongoClient()
db = client["sauce"]
users = db["users"]
