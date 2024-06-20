from flask import Blueprint, request, jsonify
from bson import ObjectId
from utils.database import products_collection

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/', methods=['GET'])
def get_all_products():
    products = list(products_collection.find({}, {'reviews': 0}))

    formatted_products = []
    for product in products:
        formatted_product = {
            'product_id': str(product['_id']),
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'category': product['category'],
            'image_url': product['image_url']
        }
        formatted_products.append(formatted_product)

    return jsonify(formatted_products), 200

@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products_collection.find_one({'_id': ObjectId(product_id)})

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    formatted_product = {
        'product_id': str(product['_id']),
        'name': product['name'],
        'description': product['description'],
        'price': product['price'],
        'category': product['category'],
        'image_url': product['image_url'],
        'reviews': product['reviews']
    }

    return jsonify(formatted_product), 200

@bp.route('/create', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category = data.get('category')
    image_url = data.get('image_url')

    if not name or not description or not price or not category or not image_url:
        return jsonify({'error': 'Name, description, price, category, and image_url are required'}), 400

    product = {
        'name': name,
        'description': description,
        'price': price,
        'category': category,
        'image_url': image_url,
        'reviews': []
    }

    result = products_collection.insert_one(product)

    if result.inserted_id:
        return jsonify({'message': 'Product created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create product'}), 500

@bp.route('/update/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category = data.get('category')
    image_url = data.get('image_url')

    if not name or not description or not price or not category or not image_url:
        return jsonify({'error': 'Name, description, price, category, and image_url are required'}), 400

    result = products_collection.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': {
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'image_url': image_url
        }}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Product updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update product'}), 500

@bp.route('/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = products_collection.delete_one({'_id': ObjectId(product_id)})

    if result.deleted_count > 0:
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete product'}), 500
