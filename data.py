from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["squareyards"]
collection = db["property_listings"]
collection.insert_one({"test": "data"})
print(list(collection.find()))