# backend/routes/errors.py

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions."""
    response = jsonify({'error': {'code': e.code, 'name': e.name, 'description': e.description}})
    response.status_code = e.code if isinstance(e, HTTPException) else 500
    return response


@errors_bp.app_errorhandler(Exception)
def handle_exception(e):
    """Handle uncaught exceptions."""
    response = jsonify({'error': {'code': 500, 'name': 'Internal Server Error', 'description': str(e)}})
    response.status_code = 500
    return response
