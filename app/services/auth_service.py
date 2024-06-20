# backend/services/auth_service.py

from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from ..models.user import User
from ..utils.database import db
from functools import wraps
from app.config.config import Config

class AuthService:
    @staticmethod
    def register_user(email, password, full_name):
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            raise ValueError('Email address already registered')

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = {
            'email': email,
            'password': hashed_password,
            'full_name': full_name,
            'created_at': datetime.utcnow()
        }

        db.users.insert_one(new_user)
        del new_user['password']
        return new_user

    @staticmethod
    def login_user(email, password):
        user = db.users.find_one({'email': email})
        if not user or not check_password_hash(user['password'], password):
            return None
        
        # Generate JWT token
        token = AuthService._generate_jwt_token(str(user['_id']))
        return {
            'token': token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'full_name': user['full_name']
            }
        }

    @staticmethod
    def _generate_jwt_token(user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRATION_DAYS']),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return token.decode('utf-8')

    @staticmethod
    def decode_jwt_token(token):
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    @staticmethod
    def get_user_by_id(user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            del user['password']
        return user

    @staticmethod
    def update_user_password(user_id, new_password):
        hashed_password = generate_password_hash(new_password, method='sha256')
        db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'password': hashed_password}})

    @staticmethod
    def delete_user(user_id):
        db.users.delete_one({'_id': ObjectId(user_id)})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Assuming the token is passed as "Bearer <JWT>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated