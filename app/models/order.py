# backend/models/order.py

from bson import ObjectId
from pymongo.collection import Collection

class Order:
    def __init__(self, db: Collection):
        self.collection = db['orders']

    async def create_order(self, order_data: dict) -> dict:
        result = await self.collection.insert_one(order_data)
        return {'id': str(result.inserted_id)}

    async def get_order_by_id(self, order_id: str) -> dict:
        order = await self.collection.find_one({'_id': ObjectId(order_id)})
        if order:
            order['_id'] = str(order['_id'])
        return order

    async def get_orders_by_user_id(self, user_id: str) -> list:
        orders = []
        async for order in self.collection.find({'user_id': user_id}):
            order['_id'] = str(order['_id'])
            orders.append(order)
        return orders

    async def update_order_status(self, order_id: str, status: str) -> dict:
        result = await self.collection.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': status}}
        )
        if result.modified_count > 0:
            return {'message': 'Order status updated successfully'}
        else:
            return {'message': 'Order not found'}

    async def delete_order(self, order_id: str) -> dict:
        result = await self.collection.delete_one({'_id': ObjectId(order_id)})
        if result.deleted_count > 0:
            return {'message': 'Order deleted successfully'}
        else:
            return {'message': 'Order not found'}
