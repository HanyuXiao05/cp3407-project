# app/members/routes.py
from flask import Blueprint, jsonify, request
import pymysql
from config import db_config

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
def get_members():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MEMBER_ID, MEMBER_Title, MEMBER_Name, MEMBER_Gender, 
                   MEMBER_DOB, MEMBER_Phone, MEMBER_Email, MEMBER_EmgContactName, 
                   MEMBER_EmgContactPhone, MEMBER_Type, MEMBER_JCID, MEMBER_JCCompUsrnme
            FROM member
            ORDER BY MEMBER_ID
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        members = []
        for row in data:
            members.append({
                'member_id': row[0],
                'title': row[1],
                'name': row[2],
                'gender': row[3],
                'dob': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'phone': row[5],
                'email': row[6],
                'emergency_contact_name': row[7],
                'emergency_contact_phone': row[8],
                'type': row[9],
                'jcid': row[10],
                'jcusername': row[11],
            })

        return jsonify({'members': members, 'count': len(members)})
    except Exception as e:
        return jsonify({'error': str(e), 'members': [], 'count': 0}), 500

@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MEMBER_ID, MEMBER_Title, MEMBER_Name, MEMBER_Gender, 
                   MEMBER_DOB, MEMBER_Phone, MEMBER_Email, MEMBER_EmgContactName, 
                   MEMBER_EmgContactPhone, MEMBER_Type
            FROM member
            WHERE MEMBER_ID = %s
        """, (member_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return jsonify({
                'member_id': row[0],
                'title': row[1],
                'name': row[2],
                'gender': row[3],
                'dob': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'phone': row[5],
                'email': row[6],
                'emergency_contact_name': row[7],
                'emergency_contact_phone': row[8],
                'type': row[9]
            })
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/search', methods=['GET'])
def search_members():
    try:
        query = request.args.get('q', '')
        member_type = request.args.get('type', '')

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        sql = """
            SELECT MEMBER_ID, MEMBER_Title, MEMBER_Name, MEMBER_Gender, 
                   MEMBER_DOB, MEMBER_Phone, MEMBER_Email, MEMBER_EmgContactName, 
                   MEMBER_EmgContactPhone, MEMBER_Type
            FROM member
            WHERE 1=1
        """
        params = []

        if query:
            sql += " AND (MEMBER_Name LIKE %s OR MEMBER_Email LIKE %s)"
            params.extend([f'%{query}%', f'%{query}%'])

        if member_type:
            sql += " AND MEMBER_Type = %s"
            params.append(member_type)

        sql += " ORDER BY MEMBER_ID"

        cursor.execute(sql, params)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        members = []
        for row in data:
            members.append({
                'member_id': row[0],
                'title': row[1],
                'name': row[2],
                'gender': row[3],
                'dob': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'phone': row[5],
                'email': row[6],
                'emergency_contact_name': row[7],
                'emergency_contact_phone': row[8],
                'type': row[9]
            })

        return jsonify({
            'members': members,
            'count': len(members),
            'query': query,
            'type_filter': member_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
