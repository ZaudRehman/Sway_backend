# backend/services/order_service.py

from bson import ObjectId
from datetime import datetime
from ..models.order import Order
from ..models.order_details import OrderDetails
from ..utils.database import db

class OrderService:
    @staticmethod
    def create_order(order_details: OrderDetails) -> str:
        new_order = {
            'user_id': order_details.user_id,
            'total_cost': order_details.total_cost,
            'cart_items': order_details.cart_items,
            'created_at': datetime.utcnow()
        }
        result = db.orders.insert_one(new_order)
        return str(result.inserted_id)

    @staticmethod
    def get_order_by_id(order_id: str) -> Order:
        order = db.orders.find_one({'_id': ObjectId(order_id)})
        return Order(**order) if order else None

    @staticmethod
    def update_order(order_id: str, order_details: OrderDetails):
        db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {
                'total_cost': order_details.total_cost,
                'cart_items': order_details.cart_items
            }}
        )

    @staticmethod
    def delete_order(order_id: str):
        db.orders.delete_one({'_id': ObjectId(order_id)})
