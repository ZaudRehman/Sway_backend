# backend/services/category_service.py

from bson import ObjectId
from ..models.category import Category
from ..utils.database import db

class CategoryService:
    @staticmethod
    def create_category(name, description):
        new_category = {
            'name': name,
            'description': description
        }
        db.categories.insert_one(new_category)

    @staticmethod
    def get_all_categories():
        categories = db.categories.find()
        return [Category(**category) for category in categories]

    @staticmethod
    def get_category_by_id(category_id):
        category = db.categories.find_one({'_id': ObjectId(category_id)})
        return Category(**category) if category else None

    @staticmethod
    def update_category(category_id, name, description):
        db.categories.update_one(
            {'_id': ObjectId(category_id)},
            {'$set': {'name': name, 'description': description}}
        )

    @staticmethod
    def delete_category(category_id):
        db.categories.delete_one({'_id': ObjectId(category_id)})
