# backend/config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGO_URI = os.getenv('MONGO_URI')
    DB_NAME = os.getenv('DATABASE_NAME')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_SENDER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def get_config():
    return Config
