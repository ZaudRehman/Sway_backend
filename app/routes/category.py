# backend/routes/category.py

from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app.services.category_service import CategoryService
from app.services.auth_service import token_required

category_bp = Blueprint('category', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = CategoryService.get_all_categories()
        return jsonify({'categories': categories}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@category_bp.route('/category', methods=['POST'])
@token_required
def add_category(current_user):
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'Category name is required'}), 400

    try:
        category = {
            'name': data['name'],
            'created_by': current_user['_id']
        }

        new_category = CategoryService.add_category(category)
        return jsonify({'message': 'Category added successfully', 'category': new_category}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@category_bp.route('/category/<string:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = CategoryService.get_category(category_id)
        if category:
            return jsonify({'category': category}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@category_bp.route('/category/<string:category_id>', methods=['PUT'])
@token_required
def update_category(current_user, category_id):
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'Category name is required'}), 400

    try:
        updated_category = CategoryService.update_category(category_id, data['name'], current_user['_id'])
        if updated_category:
            return jsonify({'message': 'Category updated successfully', 'category': updated_category}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@category_bp.route('/category/<string:category_id>', methods=['DELETE'])
@token_required
def delete_category(current_user, category_id):
    try:
        result = CategoryService.delete_category(category_id, current_user['_id'])
        if result:
            return jsonify({'message': 'Category deleted successfully'}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500
