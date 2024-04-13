from os import getenv

from pymongo import MongoClient

mongodb_client = MongoClient(getenv("MONGODB_CONNECTION_URL"))
mongodb_database = mongodb_client.get_database()
mongodb_collection = mongodb_database.get_collection("test_collection")
