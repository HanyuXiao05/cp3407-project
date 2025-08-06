from flask import jsonify
from app.errors import errors_bp

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@errors_bp.app_errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error has occurred'
    }), 500

@errors_bp.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({
        'error': 'Bad Request',
        'message': str(error.description)
    }), 400

@errors_bp.app_errorhandler(401)
def unauthorized_error(error):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication is required'
    }), 401

@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return jsonify({
        'error': 'Forbidden',
        'message': 'You do not have permission to access this resource'
    }), 403 