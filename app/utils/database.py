import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from pymongo import ReturnDocument

client = motor.motor_asyncio.AsyncIOMotorClient(config("MONGODB_URL"), w=2)
db = client["forsit"]

# Access collections
inventory_collection = db["inventory"]
sales_collection = db["sales"]
