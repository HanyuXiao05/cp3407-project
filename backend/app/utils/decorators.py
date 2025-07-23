from functools import wraps
from flask import jsonify
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({
                'error': 'Forbidden',
                'message': 'Admin privileges required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff:
            return jsonify({
                'error': 'Forbidden',
                'message': 'Staff privileges required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function 