# backend/utils/database.py

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

def get_mongo_uri():
    return os.getenv('MONGO_URI')

class Database:
    def __init__(self, app=None, db_name=None):
        self.client = None
        self.db = None

        if app is not None:
            self.init_app(app, db_name)

    def init_app(self, app, db_name=None):
        if db_name is None:
            raise ValueError("MongoDB database name must be provided")

        mongo_uri = get_mongo_uri()
        if mongo_uri is None:
            raise ValueError("MongoDB URI must be provided in the environment")

        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
        except ConnectionFailure as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")

    def get_client(self):
        if self.client is None:
            raise Exception("Database client is not initialized.")
        return self.client

    def get_db(self):
        if self.db is None:
            raise Exception("Database connection is not established.")
        return self.db

    def close(self):
        if self.client is not None:
            self.client.close()

    def initialize_collections(self, collections):
        for collection_name, options in collections.items():
            self.db.create_collection(collection_name, **options)

    def drop_collections(self, collections):
        for collection_name in collections:
            self.db.drop_collection(collection_name)

    def get_collection(self, collection_name):
        if self.db is None:
            raise Exception("Database connection is not established.")
        
        if collection_name not in self.db.list_collection_names():
            try:
                self.db.create_collection(collection_name)
            except Exception as e:
                raise Exception(f"Failed to create collection '{collection_name}': {str(e)}")
        return self.db[collection_name]

# Initialize the database instance
db = Database()
