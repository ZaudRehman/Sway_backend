# backend/routes/wishlist.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.utils.database import Database

wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route('/wishlist/<string:user_id>', methods=['GET'])
def get_wishlist(user_id):
    """Route to fetch wishlist items for a specific user."""
    try:
        db = Database()
        wishlists_collection = db.wishlists
        wishlist = wishlists_collection.find_one({'user_id': user_id})
        if wishlist:
            return jsonify(wishlist), 200
        else:
            return jsonify({'error': 'Wishlist not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@wishlist_bp.route('/wishlist/<string:user_id>', methods=['POST'])
def add_to_wishlist(user_id):
    """Route to add an item to the wishlist for a specific user."""
    try:
        wishlist_data = request.get_json()
        db = Database()
        wishlists_collection = db.wishlists
        result = wishlists_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'items': wishlist_data}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            return jsonify({'message': 'Item added to wishlist successfully'}), 200
        else:
            return jsonify({'error': 'Failed to add item to wishlist'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@wishlist_bp.route('/wishlist/<string:user_id>/<string:item_id>', methods=['DELETE'])
def remove_from_wishlist(user_id, item_id):
    """Route to remove an item from the wishlist for a specific user."""
    try:
        db = Database()
        wishlists_collection = db.wishlists
        result = wishlists_collection.update_one(
            {'user_id': user_id},
            {'$pull': {'items': {'item_id': item_id}}},
        )
        if result.modified_count > 0:
            return jsonify({'message': 'Item removed from wishlist successfully'}), 200
        else:
            return jsonify({'error': 'Item not found in wishlist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
