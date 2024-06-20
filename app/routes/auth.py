from flask import Blueprint, jsonify, request, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
from bson.objectid import ObjectId
from app.config.config import Config
from app.services.user_service import UserService
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from app.utils.database import db

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

# Create MongoClient and UserService instance
client = MongoClient(Config.MONGO_URI)
user_service = UserService(client, Config.DB_NAME, 'users')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = user_service.get_user_by_id(data['user_id'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = {
        'username': data['username'],
        'password': hashed_password,
        'email': data['email'],
        'created_at': datetime.utcnow(),
    }

    try:
        user_id = user_service.add_user(new_user)
        return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = user_service.find_one_by_username(auth.username)

    if not user or not bcrypt.check_password_hash(user['password'], auth.password):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(hours=24)}, Config.SECRET_KEY, algorithm="HS256")
    
    return jsonify({'token': token.decode('utf-8')}), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout_user(current_user):
    # Implement logout functionality as needed (e.g., token blacklist, session management)
    return jsonify({'message': 'User logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({'username': current_user['username'], 'email': current_user['email']}), 200
