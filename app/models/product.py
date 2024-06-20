# backend/models/product.py

from bson import ObjectId
from pymongo.collection import Collection

class Product:
    def __init__(self, db: Collection):
        self.collection = db['products']

    async def create_product(self, product_data: dict) -> dict:
        result = await self.collection.insert_one(product_data)
        return {'id': str(result.inserted_id)}

    async def get_product_by_id(self, product_id: str) -> dict:
        product = await self.collection.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])
        return product

    async def update_product(self, product_id: str, updated_data: dict) -> dict:
        result = await self.collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': updated_data}
        )
        if result.modified_count > 0:
            return {'message': 'Product updated successfully'}
        else:
            return {'message': 'Product not found'}

    async def delete_product(self, product_id: str) -> dict:
        result = await self.collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count > 0:
            return {'message': 'Product deleted successfully'}
        else:
            return {'message': 'Product not found'}

    async def get_products_by_category(self, category_id: str) -> list:
        products = []
        async for product in self.collection.find({'category_id': category_id}):
            product['_id'] = str(product['_id'])
            products.append(product)
        return products

    async def get_all_products(self) -> list:
        products = []
        async for product in self.collection.find():
            product['_id'] = str(product['_id'])
            products.append(product)
        return products
