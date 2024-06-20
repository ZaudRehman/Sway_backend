from flask import Blueprint, request, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime, timedelta
from app.utils.database import Database
from flask_bcrypt import Bcrypt
import jwt
import random
from flask_mail import Mail, Message
from app.config.config import Config

bp = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()
mail = Mail()

@bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    existing_user = Database.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }

    result = Database.insert_one(new_user)
    if result.inserted_id:
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'error': 'Failed to register user'}), 500

@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = Database.find_one({'email': email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id'] = str(user['_id'])
    return jsonify({'message': 'Login successful'}), 200


@bp.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = Database.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    otp = random.randint(100000, 999999)
    Database.update_one({'_id': user['_id']}, {'$set': {'otp': otp, 'otp_created_at': datetime.utcnow()}})

    msg = Message('Your OTP Code', sender=Config.MAIL_USERNAME, recipients=[email])
    msg.body = f'Your OTP code is {otp}'
    mail.send(msg)

    return jsonify({'message': 'OTP sent successfully'}), 200

@bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({'error': 'Email and OTP are required'}), 400

    user = Database.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user['otp'] == int(otp) and (datetime.utcnow() - user['otp_created_at']).seconds < 300:
        session['user_id'] = str(user['_id'])
        return jsonify({'message': 'OTP verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid or expired OTP'}), 401


@bp.route('/logout', methods=['POST'])
def logout_user():
    if 'user_id' in session:
        session.pop('user_id', None)
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'User not logged in'}), 401

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = Database.find_one({'_id': ObjectId(user_id)})
    else:
        g.user = None

@bp.route('/profile', methods=['GET'])
def get_user_profile():
    if g.user:
        user_profile = {
            'username': g.user['username'],
            'email': g.user['email'],
            'created_at': g.user['created_at'],
            'updated_at': g.user['updated_at']
        }
        return jsonify(user_profile), 200
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@bp.route('/profile/update', methods=['PUT'])
def update_user_profile():
    if not g.user:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.json
    new_email = data.get('email')

    if not new_email:
        return jsonify({'error': 'New email is required'}), 400

    existing_user = Database.find_one({'email': new_email})
    if existing_user and existing_user['_id'] != g.user['_id']:
        return jsonify({'error': 'Email already registered'}), 400

    result = Database.update_one(
        {'_id': g.user['_id']},
        {'$set': {'email': new_email, 'updated_at': datetime.utcnow()}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update profile'}), 500

@bp.route('/profile/delete', methods=['DELETE'])
def delete_user_profile():
    if not g.user:
        return jsonify({'error': 'User not authenticated'}), 401

    result = Database.delete_one({'_id': g.user['_id']})

    if result.deleted_count > 0:
        session.pop('user_id', None)
        return jsonify({'message': 'Profile deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete profile'}), 500
