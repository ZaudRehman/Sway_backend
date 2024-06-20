# backend/services/db_service.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseService:
    def __init__(self, db_uri: str, db_name: str):
        try:
            self.client = MongoClient(db_uri)
            self.db = self.client[db_name]
        except ConnectionFailure as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")

    def get_client(self) -> MongoClient:
        return self.client

    def get_database(self):
        return self.db

    def close_connection(self):
        self.client.close()

    def initialize_collections(self, collections: dict):
        for name, options in collections.items():
            self.db.create_collection(name, **options)

    def drop_collections(self, collections: list):
        for name in collections:
            self.db.drop_collection(name)
