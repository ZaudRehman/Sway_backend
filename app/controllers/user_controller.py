from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from utils.database import users_collection

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    hashed_password = generate_password_hash(password)

    user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }

    try:
        result = users_collection.insert_one(user)
        if result.inserted_id:
            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify({'error': 'Failed to register user'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to register user: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = users_collection.find_one({'email': email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id'] = str(user['_id'])
    return jsonify({'message': 'Login successful'}), 200

@bp.route('/profile', methods=['GET'])
def get_user_profile():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    user = users_collection.find_one({'_id': ObjectId(user_id)}, {'password': 0})

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': user}), 200

@bp.route('/profile/update', methods=['PUT'])
def update_user_profile():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.json
    new_username = data.get('username')
    new_email = data.get('email')

    if not new_username and not new_email:
        return jsonify({'error': 'Nothing to update'}), 400

    update_fields = {}
    if new_username:
        update_fields['username'] = new_username
    if new_email:
        update_fields['email'] = new_email

    try:
        result = users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_fields}
        )

        if result.modified_count > 0:
            return jsonify({'message': 'User profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update user profile'}), 500

    except Exception as e:
        return jsonify({'error': f'Failed to update user profile: {str(e)}'}), 500

@bp.route('/delete', methods=['DELETE'])
def delete_user_account():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    try:
        result = users_collection.delete_one({'_id': ObjectId(user_id)})

        if result.deleted_count > 0:
            # Optionally, you may want to clear session data upon deletion
            session.clear()
            return jsonify({'message': 'User account deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete user account'}), 500

    except Exception as e:
        return jsonify({'error': f'Failed to delete user account: {str(e)}'}), 500

# Add more endpoints as needed for user management

