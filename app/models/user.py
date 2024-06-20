# backend/models/user.py
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection

class User:

    def __init__(self, username, email, password, created_at=None, updated_at=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __init__(self, db: Collection):
        self.collection = db['users']

    async def create_user(self, user_data: dict) -> dict:
        result = await self.collection.insert_one(user_data)
        return {'id': str(result.inserted_id)}

    async def get_user_by_id(self, user_id: str) -> dict:
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
        return user

    async def update_user(self, user_id: str, updated_data: dict) -> dict:
        result = await self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': updated_data}
        )
        if result.modified_count > 0:
            return {'message': 'User updated successfully'}
        else:
            return {'message': 'User not found'}

    async def delete_user(self, user_id: str) -> dict:
        result = await self.collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return {'message': 'User deleted successfully'}
        else:
            return {'message': 'User not found'}

    async def get_user_by_email(self, email: str) -> dict:
        user = await self.collection.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
        return user
