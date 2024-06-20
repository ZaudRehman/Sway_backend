# backend/routes/products.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.utils.database import Database
from app.models.product import Product

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_products():
    """Route to fetch all products."""
    try:
        db = Database()
        products_collection = db.products
        products = list(products_collection.find())
        return jsonify({'products': products}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    """Route to fetch a specific product by its ID."""
    try:
        db = Database()
        products_collection = db.products
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if product:
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products', methods=['POST'])
def create_product():
    """Route to create a new product."""
    try:
        product_data = request.get_json()
        new_product = Product(**product_data)  # Assuming Product model is used
        db = Database()
        products_collection = db.products
        result = products_collection.insert_one(new_product.to_dict())
        return jsonify({'message': 'Product created successfully', 'product_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    """Route to update an existing product."""
    try:
        product_data = request.get_json()
        db = Database()
        products_collection = db.products
        result = products_collection.update_one({'_id': ObjectId(product_id)}, {'$set': product_data})
        if result.modified_count > 0:
            return jsonify({'message': 'Product updated successfully'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Route to delete a product."""
    try:
        db = Database()
        products_collection = db.products
        result = products_collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
