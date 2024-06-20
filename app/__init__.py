from flask import Flask
from app.utils.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app
