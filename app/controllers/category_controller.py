from flask import Blueprint, request, jsonify
from bson import ObjectId
from utils.database import categories_collection

bp = Blueprint('category', __name__, url_prefix='/category')

@bp.route('/', methods=['GET'])
def get_all_categories():
    categories = list(categories_collection.find({}, {'name': 1, 'description': 1}))

    formatted_categories = []
    for category in categories:
        formatted_category = {
            'category_id': str(category['_id']),
            'name': category['name'],
            'description': category['description']
        }
        formatted_categories.append(formatted_category)

    return jsonify(formatted_categories), 200

@bp.route('/<category_id>', methods=['GET'])
def get_category(category_id):
    category = categories_collection.find_one({'_id': ObjectId(category_id)})

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    formatted_category = {
        'category_id': str(category['_id']),
        'name': category['name'],
        'description': category['description']
    }

    return jsonify(formatted_category), 200

@bp.route('/create', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required'}), 400

    category = {
        'name': name,
        'description': description
    }

    result = categories_collection.insert_one(category)

    if result.inserted_id:
        return jsonify({'message': 'Category created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create category'}), 500

@bp.route('/update/<category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required'}), 400

    result = categories_collection.update_one(
        {'_id': ObjectId(category_id)},
        {'$set': {'name': name, 'description': description}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Category updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update category'}), 500

@bp.route('/delete/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    result = categories_collection.delete_one({'_id': ObjectId(category_id)})

    if result.deleted_count > 0:
        return jsonify({'message': 'Category deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete category'}), 500
