# app/membership_type/routes.py

from flask import Blueprint, jsonify
from app.models.membership_type import MembershipType

membership_type_bp = Blueprint('membership_type', __name__)

@membership_type_bp.route('/', methods=['GET'])
def get_all_membership_types():
    types = MembershipType.query.all()
    return jsonify({
        'types': [t.to_dict() for t in types],
        'count': len(types)
    })
