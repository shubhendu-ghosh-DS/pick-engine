from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["electronics_db"]

# collections
ac_collection = db["ac"]
tv_collection = db["tv"]
fridge_collection = db["fridge"]
wash_collection = db["wash"]
appliance_collection = db["appliances"]