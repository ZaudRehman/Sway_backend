# backend/models/cart.py

from typing import List
from pydantic import BaseModel

class CartItem(BaseModel):
    product_id: str
    quantity: int

class Cart(BaseModel):
    user_id: str
    items: List[CartItem]

    class Config:
        orm_mode = True

# You can also keep the database interaction methods separately
# if you don't want to mix them with the Pydantic models
from app.utils.database import db

class CartDB:
    @staticmethod
    def get_collection():
        return db.get_collection('carts')

    @classmethod
    def add_item(cls, user_id, product_id, quantity):
        collection = cls.get_collection()
        cart = collection.find_one({"user_id": user_id})
        if cart:
            items = cart.get('items', [])
            items.append({"product_id": product_id, "quantity": quantity})
            collection.update_one({"user_id": user_id}, {"$set": {"items": items}})
        else:
            collection.insert_one({"user_id": user_id, "items": [{"product_id": product_id, "quantity": quantity}]})

    @classmethod
    def get_cart(cls, user_id):
        collection = cls.get_collection()
        return collection.find_one({"user_id": user_id}, {'_id': 0})
