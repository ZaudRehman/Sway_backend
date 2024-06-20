# backend/routes/orders.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.utils.database import Database
from app.models.order import Order

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Route to fetch all orders."""
    try:
        db = Database()
        orders_collection = db.orders
        orders = list(orders_collection.find())
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """Route to fetch a specific order by its ID."""
    try:
        db = Database()
        orders_collection = db.orders
        order = orders_collection.find_one({'_id': ObjectId(order_id)})
        if order:
            return jsonify(order), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Route to create a new order."""
    try:
        order_data = request.get_json()
        new_order = Order(**order_data)  # Assuming Order model is used
        db = Database()
        orders_collection = db.orders
        result = orders_collection.insert_one(new_order.to_dict())
        return jsonify({'message': 'Order created successfully', 'order_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<string:order_id>', methods=['PUT'])
def update_order(order_id):
    """Route to update an existing order."""
    try:
        order_data = request.get_json()
        db = Database()
        orders_collection = db.orders
        result = orders_collection.update_one({'_id': ObjectId(order_id)}, {'$set': order_data})
        if result.modified_count > 0:
            return jsonify({'message': 'Order updated successfully'}), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Route to delete an order."""
    try:
        db = Database()
        orders_collection = db.orders
        result = orders_collection.delete_one({'_id': ObjectId(order_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Order deleted successfully'}), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
