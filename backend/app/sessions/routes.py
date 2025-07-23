# app/sessions/routes.py
from flask import Blueprint, jsonify
import pymysql
from config import db_config

sessions_bp = Blueprint('sessions', __name__)

@sessions_bp.route('/', methods=['GET'])
def get_sessions():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SESSION_ID, SESSION_Date, SESSION_Time, SESSION_Capacity
            FROM session
            ORDER BY SESSION_Date, SESSION_Time
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        sessions = []
        for row in data:
            sessions.append({
                'session_id': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else None,
                'time': str(row[2]) if row[2] else None,
                'capacity': row[3]
            })

        return jsonify({'sessions': sessions, 'count': len(sessions)})
    except Exception as e:
        return jsonify({'error': str(e), 'sessions': [], 'count': 0}), 500

@sessions_bp.route('/<int:session_id>', methods=['GET'])
def get_session(session_id):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SESSION_ID, SESSION_Date, SESSION_Time, SESSION_Capacity
            FROM session
            WHERE SESSION_ID = %s
        """, (session_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return jsonify({
                'session_id': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else None,
                'time': str(row[2]) if row[2] else None,
                'capacity': row[3]
            })
        else:
            return jsonify({'error': 'Session not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
