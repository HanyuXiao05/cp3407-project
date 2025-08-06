# app/booking/routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import pymysql

from app import db
from config import db_config  # 你可以从 config.py 暴露 db_config 或 utils

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/', methods=['GET'])
def get_bookings():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, 
                   BOOKING_Time, BOOKING_Status
            FROM booking
            ORDER BY BOOKING_Date DESC, BOOKING_Time DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        bookings = []
        for row in data:
            bookings.append({
                'booking_ref': row[0],
                'member_id': row[1],
                'session_id': row[2],
                'booking_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'booking_time': str(row[4]) if row[4] else None,
                'status': row[5]
            })

        return jsonify({'bookings': bookings, 'count': len(bookings)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/', methods=['POST'])
@login_required
def create_booking():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        booking_date = data.get('booking_date')  # format: "YYYY-MM-DD"
        booking_time = data.get('booking_time')  # format: "HH:MM"
        status = data.get('status', 'Pending')

        if not session_id or not booking_date or not booking_time:
            return jsonify({'error': 'Missing required fields'}), 400

        booking_ref = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            booking_ref,
            current_user.MEMBER_ID,
            session_id,
            booking_date,
            booking_time,
            status
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Booking created', 'booking_ref': booking_ref}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/<booking_ref>', methods=['PUT'])
@login_required
def update_booking(booking_ref):
    try:
        data = request.get_json()

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT MEMBER_ID FROM booking WHERE BOOKING_Ref = %s", (booking_ref,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Booking not found'}), 404
        if result[0] != current_user.MEMBER_ID:
            return jsonify({'error': 'Unauthorized'}), 403

        fields = []
        values = []

        if 'session_id' in data:
            fields.append("SESSION_ID = %s")
            values.append(data['session_id'])
        if 'booking_date' in data:
            fields.append("BOOKING_Date = %s")
            values.append(data['booking_date'])
        if 'booking_time' in data:
            fields.append("BOOKING_Time = %s")
            values.append(data['booking_time'])
        if 'status' in data:
            fields.append("BOOKING_Status = %s")
            values.append(data['status'])

        if not fields:
            return jsonify({'error': 'No fields to update'}), 400

        values.append(booking_ref)
        sql = f"UPDATE booking SET {', '.join(fields)} WHERE BOOKING_Ref = %s"

        cursor.execute(sql, tuple(values))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Booking updated'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/<booking_ref>', methods=['DELETE'])
@login_required
def delete_booking(booking_ref):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT MEMBER_ID FROM booking WHERE BOOKING_Ref = %s", (booking_ref,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Booking not found'}), 404
        if result[0] != current_user.MEMBER_ID:
            return jsonify({'error': 'Unauthorized'}), 403

        cursor.execute("DELETE FROM booking WHERE BOOKING_Ref = %s", (booking_ref,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Booking deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
