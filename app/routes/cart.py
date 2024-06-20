# backend/routes/cart.py

from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app.services.cart_service import CartService
from app.services.auth_service import token_required

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    data = request.get_json()

    if 'product_id' not in data or 'quantity' not in data:
        return jsonify({'message': 'Missing fields'}), 400

    try:
        cart_item = {
            'user_id': current_user['_id'],
            'product_id': ObjectId(data['product_id']),
            'quantity': int(data['quantity']),
        }

        CartService.add_to_cart(cart_item)
        return jsonify({'message': 'Item added to cart successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@cart_bp.route('/update/<string:cart_item_id>', methods=['PUT'])
@token_required
def update_cart_item(current_user, cart_item_id):
    data = request.get_json()

    if 'quantity' not in data:
        return jsonify({'message': 'Missing fields'}), 400

    try:
        CartService.update_cart_item(current_user['_id'], cart_item_id, int(data['quantity']))
        return jsonify({'message': 'Cart item updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@cart_bp.route('/remove/<string:cart_item_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, cart_item_id):
    try:
        CartService.remove_from_cart(current_user['_id'], cart_item_id)
        return jsonify({'message': 'Item removed from cart successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@cart_bp.route('/', methods=['GET'])
@token_required
def get_cart(current_user):
    try:
        cart_items = CartService.get_cart_items(current_user['_id'])
        return jsonify({'cart_items': cart_items}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500
