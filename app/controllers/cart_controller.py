from flask import Blueprint, request, jsonify, g
from bson import ObjectId
from datetime import datetime
from utils.database import carts_collection

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/add', methods=['POST'])
def add_to_cart():
    if not g.user:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    cart_item = {
        'user_id': ObjectId(g.user['_id']),
        'product_id': ObjectId(product_id),
        'quantity': quantity,
        'added_at': datetime.utcnow()
    }

    result = carts_collection.insert_one(cart_item)
    if result.inserted_id:
        return jsonify({'message': 'Item added to cart successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add item to cart'}), 500

@bp.route('/list', methods=['GET'])
def list_cart_items():
    if not g.user:
        return jsonify({'error': 'User not authenticated'}), 401

    user_id = ObjectId(g.user['_id'])
    cart_items = list(carts_collection.find({'user_id': user_id}))

    formatted_cart_items = []
    for item in cart_items:
        formatted_item = {
            'cart_item_id': str(item['_id']),
            'product_id': str(item['product_id']),
            'quantity': item['quantity'],
            'added_at': item['added_at']
        }
        formatted_cart_items.append(formatted_item)

    return jsonify(formatted_cart_items), 200

@bp.route('/update', methods=['PUT'])
def update_cart_item():
    if not g.user:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.json
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity')

    if not cart_item_id or not quantity:
        return jsonify({'error': 'Cart item ID and quantity are required'}), 400

    result = carts_collection.update_one(
        {'_id': ObjectId(cart_item_id), 'user_id': ObjectId(g.user['_id'])},
        {'$set': {'quantity': quantity}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Cart item updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update cart item'}), 500

@bp.route('/remove', methods=['DELETE'])
def remove_from_cart():
    if not g.user:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.json
    cart_item_id = data.get('cart_item_id')

    if not cart_item_id:
        return jsonify({'error': 'Cart item ID is required'}), 400

    result = carts_collection.delete_one(
        {'_id': ObjectId(cart_item_id), 'user_id': ObjectId(g.user['_id'])}
    )

    if result.deleted_count > 0:
        return jsonify({'message': 'Cart item removed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to remove cart item'}), 500
