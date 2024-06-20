from flask import Blueprint, request, jsonify
from bson import ObjectId
from utils.database import orders_collection

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/', methods=['GET'])
def get_all_orders():
    orders = list(orders_collection.find({}, {'order_items': 0}))

    formatted_orders = []
    for order in orders:
        formatted_order = {
            'order_id': str(order['_id']),
            'user_id': order['user_id'],
            'total_cost': order['total_cost'],
            'status': order['status']
        }
        formatted_orders.append(formatted_order)

    return jsonify(formatted_orders), 200

@bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders_collection.find_one({'_id': ObjectId(order_id)})

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    formatted_order = {
        'order_id': str(order['_id']),
        'user_id': order['user_id'],
        'total_cost': order['total_cost'],
        'status': order['status'],
        'order_items': order['order_items']
    }

    return jsonify(formatted_order), 200

@bp.route('/create', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    total_cost = data.get('total_cost')
    order_items = data.get('order_items', [])
    status = data.get('status', 'Pending')

    if not user_id or not total_cost:
        return jsonify({'error': 'User ID and total cost are required'}), 400

    order = {
        'user_id': user_id,
        'total_cost': total_cost,
        'order_items': order_items,
        'status': status
    }

    result = orders_collection.insert_one(order)

    if result.inserted_id:
        return jsonify({'message': 'Order created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create order'}), 500

@bp.route('/update/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    total_cost = data.get('total_cost')
    order_items = data.get('order_items')
    status = data.get('status')

    if not total_cost or not order_items or not status:
        return jsonify({'error': 'Total cost, order items, and status are required'}), 400

    result = orders_collection.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {'total_cost': total_cost, 'order_items': order_items, 'status': status}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Order updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update order'}), 500

@bp.route('/delete/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    result = orders_collection.delete_one({'_id': ObjectId(order_id)})

    if result.deleted_count > 0:
        return jsonify({'message': 'Order deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete order'}), 500
