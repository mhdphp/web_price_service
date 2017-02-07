import pymongo
import os

class Database(object):

    # URI = "mongodb://127.0.0.1:27017"
    # for deployment on Heroku
    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None


    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)


    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)


    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)


    @staticmethod
    def update(collection, query, data):
        # upsert=True, if don't find an element with query, then insert the data
        Database.DATABASE[collection].update(query, data, upsert=True)


    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)


