# backend/services/cart_service.py

from bson import ObjectId
from app.models.cart import Cart
from ..utils.database import db

class CartService:
    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        # Check if the product is already in the cart
        existing_item = db.cart.find_one({'user_id': user_id, 'product_id': product_id})
        if existing_item:
            # Update the quantity of the existing item
            db.cart.update_one({'_id': existing_item['_id']}, {'$set': {'quantity': existing_item['quantity'] + quantity}})
        else:
            # Add new item to the cart
            new_item = {
                'user_id': user_id,
                'product_id': product_id,
                'quantity': quantity
            }
            db.cart.insert_one(new_item)

    @staticmethod
    def get_cart_items(user_id):
        cart_items = db.cart.find({'user_id': user_id})
        return [Cart(**item) for item in cart_items]

    @staticmethod
    def update_cart_item(user_id, item_id, quantity):
        db.cart.update_one({'_id': ObjectId(item_id), 'user_id': user_id}, {'$set': {'quantity': quantity}})

    @staticmethod
    def remove_from_cart(user_id, item_id):
        db.cart.delete_one({'_id': ObjectId(item_id), 'user_id': user_id})

    @staticmethod
    def clear_cart(user_id):
        db.cart.delete_many({'user_id': user_id})
