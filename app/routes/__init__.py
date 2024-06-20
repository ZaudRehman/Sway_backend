# backend/routes/__init__.py

from flask import Blueprint
from .auth import auth_bp
from .products import products_bp
from .cart import cart_bp
from .category import category_bp
from .orders import orders_bp
from .wishlist import wishlist_bp
from .error import errors_bp

def initialize_routes(app):
    """
    Initialize routes for the Flask application.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(errors_bp)
