# backend/app.py

from flask import Flask, jsonify
from app.utils.database import db
from flask_mail import Mail
from app.config.config import get_config
from app.controllers.auth_controller import bp as auth_bp
import os

# Initialize the Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(get_config())

# Initialize the database with the application and the database name
db.init_app(app, db_name="sway")
mail = Mail(app)
# Import blueprints (after db initialization)
from app.routes.auth import auth_bp
from app.routes.products import products_bp
from app.routes.cart import cart_bp
from app.routes.orders import orders_bp
from app.routes.wishlist import wishlist_bp
from app.routes.category import category_bp
from app.routes.error import errors_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(errors_bp)  # No URL prefix for errors

# Define a route to test the database connection
@app.route('/')
def test_db_connection():
    try:
        client = db.get_client()
        db_name = db.get_db().name
        return jsonify({
            'message': 'Database connection successful!',
            'database_name': db_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define a route for health check
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
