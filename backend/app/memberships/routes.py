# app/memberships/routes.py
from flask import Blueprint, jsonify
import pymysql
from config import db_config

memberships_bp = Blueprint('memberships', __name__)

@memberships_bp.route('/', methods=['GET'])
def get_memberships():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MEMBERSHIP_ID, MEMBER_ID, MEM_TYPE_ID, MEMBERSHIP_StartDate, 
                   MEMBERSHIP_ExpDate, MEMBERSHIP_Declared
            FROM membership
            ORDER BY MEMBERSHIP_ID
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        memberships = []
        for row in data:
            memberships.append({
                'membership_id': row[0],
                'member_id': row[1],
                'membership_type_id': row[2],
                'start_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'expiry_date': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'declared': bool(row[5])
            })

        return jsonify({'memberships': memberships, 'count': len(memberships)})
    except Exception as e:
        return jsonify({'error': str(e), 'memberships': [], 'count': 0}), 500

@memberships_bp.route('/types', methods=['GET'])
def get_membership_types():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MEM_TYPE_ID, MEM_TYPE_Name, MEM_TYPE_Fee
            FROM membership_type
            ORDER BY MEM_TYPE_ID
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        types = []
        for row in data:
            types.append({
                'type_id': row[0],
                'name': row[1],
                'fee': float(row[2])
            })

        return jsonify({'membership_types': types, 'count': len(types)})
    except Exception as e:
        return jsonify({'error': str(e), 'membership_types': [], 'count': 0}), 500
