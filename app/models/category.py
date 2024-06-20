# backend/models/category.py

from bson import ObjectId
from pymongo.collection import Collection

class Category:
    def __init__(self, db: Collection):
        self.collection = db['categories']

    async def create_category(self, category_data: dict) -> dict:
        result = await self.collection.insert_one(category_data)
        return {'id': str(result.inserted_id)}

    async def get_category_by_id(self, category_id: str) -> dict:
        category = await self.collection.find_one({'_id': ObjectId(category_id)})
        if category:
            category['_id'] = str(category['_id'])
        return category

    async def get_all_categories(self) -> list:
        categories = []
        async for category in self.collection.find():
            category['_id'] = str(category['_id'])
            categories.append(category)
        return categories

    async def update_category(self, category_id: str, category_data: dict) -> dict:
        result = await self.collection.update_one(
            {'_id': ObjectId(category_id)},
            {'$set': category_data}
        )
        if result.modified_count > 0:
            return {'message': 'Category updated successfully'}
        else:
            return {'message': 'Category not found'}

    async def delete_category(self, category_id: str) -> dict:
        result = await self.collection.delete_one({'_id': ObjectId(category_id)})
        if result.deleted_count > 0:
            return {'message': 'Category deleted successfully'}
        else:
            return {'message': 'Category not found'}
