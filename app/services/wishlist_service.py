# backend/services/wishlist_service.py

from typing import List
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from ..models.product import Product
from ..models.user import User

class WishlistService:
    def __init__(self, client: MongoClient, db_name: str, collection_name: str):
        self.db = client[db_name]
        self.collection: Collection = self.db[collection_name]

    def get_user_wishlist(self, user_id: str) -> List[Product]:
        try:
            user_wishlist = self.collection.find_one({"user_id": ObjectId(user_id)})
            if user_wishlist:
                return [Product(**item) for item in user_wishlist.get('wishlist', [])]
            else:
                return []
        except PyMongoError as e:
            raise Exception(f"Failed to fetch wishlist: {str(e)}")

    def add_to_wishlist(self, user_id: str, product: Product) -> None:
        try:
            self.collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$addToSet": {"wishlist": product.dict()}}
            )
        except PyMongoError as e:
            raise Exception(f"Failed to add to wishlist: {str(e)}")

    def remove_from_wishlist(self, user_id: str, product_id: str) -> None:
        try:
            self.collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$pull": {"wishlist": {"product_id": ObjectId(product_id)}}}
            )
        except PyMongoError as e:
            raise Exception(f"Failed to remove from wishlist: {str(e)}")

    def clear_wishlist(self, user_id: str) -> None:
        try:
            self.collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$set": {"wishlist": []}}
            )
        except PyMongoError as e:
            raise Exception(f"Failed to clear wishlist: {str(e)}")
