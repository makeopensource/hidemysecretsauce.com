import pymongo

client = pymongo.MongoClient("mongodb://mongo:27017/")

db = client["sauce"]

users = db["users"]