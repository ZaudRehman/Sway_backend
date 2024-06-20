from flask import Flask
from flask_mail import Mail
from app.utils.database import db
from app.config.config import get_config, Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    mail = Mail(app)
    db.init_app(app, db_name=Config.DB_NAME)
    
    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app
