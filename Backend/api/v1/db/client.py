### MongoDB client ###

from pymongo import MongoClient

# BD Mongo local
db_client = MongoClient().local.drops
