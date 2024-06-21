from flask import Blueprint, jsonify, request, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
from bson.objectid import ObjectId
from app.config.config import Config
from app.utils.email_service import send_otp_email
from app.services.user_service import UserService
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from app.utils.database import db
import random

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

# Create MongoClient and UserService instance
client = MongoClient(Config.MONGO_URI)
user_service = UserService(client, Config.DB_NAME, 'users')
users_collection = db.get_collection('users')

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
        otp = ''.join([random.choice(string.digits) for _ in range(6)])
        
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"otp": otp, "is_verified": False}}
        )

        send_otp_email(data['email'], otp)

        return jsonify({'message': 'OTP Sent to your email', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp_entered = data.get('otp')

    if not email or not otp_entered:
        return jsonify({'error': 'Email and OTP are required'}), 400

    user = users_collection.find_one({'email': email})

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user['otp'] == otp_entered:
        users_collection.update_one({'_id': user['_id']}, {'$set': {'is_verified': True}})

        return jsonify({'message': 'OTP verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 400

def generate_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return make_response(jsonify({'message': 'Email and password are required'}), 400)

    user = users_collection.find_one({'email': email})

    if not user or not bcrypt.check_password_hash(user['password'], password):
        return make_response(jsonify({'message': 'Invalid credentials'}), 401)

    if not user.get('is_verified', False):
        return make_response(jsonify({'message': 'Email is not verified'}), 401)

    token = generate_token(user['_id'])

    return jsonify({'token': token}), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout_user(current_user):
    # Implement logout functionality as needed (e.g., token blacklist, session management)
    return jsonify({'message': 'User logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({'username': current_user['username'], 'email': current_user['email']}), 200
