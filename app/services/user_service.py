# backend/services/user_service.py

from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from ..models.user import User

class UserService:
    def __init__(self, client: MongoClient, db_name: str, collection_name: str):
        self.db = client[db_name]
        self.collection: Collection = self.db[collection_name]

    def get_all_users(self) -> List[User]:
        try:
            users = self.collection.find()
            return [User(**user) for user in users]
        except PyMongoError as e:
            raise Exception(f"Failed to fetch users: {str(e)}")

    def get_user_by_id(self, user_id: str) -> User:
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return User(**user)
            else:
                raise Exception("User not found")
        except PyMongoError as e:
            raise Exception(f"Failed to fetch user: {str(e)}")
        
    
    def find_one_by_username(self, username: str) -> Optional[User]:
        try:
            user = self.collection.find_one({"username": username})
            if user:
                # Ensure password field contains the bcrypt hashed password
                if 'password' in user:
                    hashed_password = user['password']
                    return User(username=user['username'], password=hashed_password, email=user['email'])
                else:
                    raise Exception("User document does not contain 'password' field")
            else:
                return None
        except PyMongoError as e:
            raise Exception(f"Failed to fetch user by username: {str(e)}")


    def add_user(self, user: dict) -> str:
        existing_user = self.collection.find_one({"$or": [{"username": user['username']}, {"email": user['email']}]})
        if existing_user:
            raise Exception("Username or email already exists")

        try:
            result = self.collection.insert_one(user)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to add user: {str(e)}")


    def update_user(self, user_id: str, updated_user: User) -> None:
        try:
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user.dict()})
        except PyMongoError as e:
            raise Exception(f"Failed to update user: {str(e)}")

    def delete_user(self, user_id: str) -> None:
        try:
            self.collection.delete_one({"_id": ObjectId(user_id)})
        except PyMongoError as e:
            raise Exception(f"Failed to delete user: {str(e)}")
