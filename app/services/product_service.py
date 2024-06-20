# backend/services/product_service.py

from typing import List
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from ..models.product import Product

class ProductService:
    def __init__(self, client: MongoClient, db_name: str, collection_name: str):
        self.db = client[db_name]
        self.collection: Collection = self.db[collection_name]

    def get_all_products(self) -> List[Product]:
        try:
            products = self.collection.find()
            return [Product(**product) for product in products]
        except PyMongoError as e:
            raise Exception(f"Failed to fetch products: {str(e)}")

    def get_product_by_id(self, product_id: str) -> Product:
        try:
            product = self.collection.find_one({"_id": ObjectId(product_id)})
            if product:
                return Product(**product)
            else:
                raise Exception("Product not found")
        except PyMongoError as e:
            raise Exception(f"Failed to fetch product: {str(e)}")

    def add_product(self, product: Product) -> str:
        try:
            result = self.collection.insert_one(product.dict())
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to add product: {str(e)}")

    def update_product(self, product_id: str, updated_product: Product) -> None:
        try:
            self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": updated_product.dict()})
        except PyMongoError as e:
            raise Exception(f"Failed to update product: {str(e)}")

    def delete_product(self, product_id: str) -> None:
        try:
            self.collection.delete_one({"_id": ObjectId(product_id)})
        except PyMongoError as e:
            raise Exception(f"Failed to delete product: {str(e)}")
