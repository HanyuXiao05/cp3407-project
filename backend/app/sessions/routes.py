# app/sessions/routes.py
from flask import Blueprint, jsonify, request
import pymysql
from config import db_config
from datetime import datetime, timedelta

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

@sessions_bp.route('/availability', methods=['GET'])
def get_slot_availability():
    """Get real-time slot availability for a specific date"""
    try:
        date = request.args.get('date')
        user_type = request.args.get('user_type', 'student')
        
        if not date:
            return jsonify({'error': 'Date parameter is required'}), 400

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Get all bookings for the specified date
        cursor.execute("""
            SELECT b.BOOKING_Time, COUNT(*) as booked_count
            FROM booking b
            WHERE b.BOOKING_Date = %s AND b.BOOKING_Status != 'Cancelled'
            GROUP BY b.BOOKING_Time
        """, (date,))
        
        booked_slots = {}
        for row in cursor.fetchall():
            booked_slots[row[0]] = row[1]

        # Generate available time slots based on user type
        slots = generate_available_slots(date, user_type)
        
        # Calculate availability for each slot
        availability = []
        for slot in slots:
            time_range = slot.split(' - ')
            start_time = time_range[0]
            booked_count = booked_slots.get(start_time, 0)
            available_spots = 6 - booked_count  # Max 6 people per session
            
            availability.append({
                'time_slot': slot,
                'start_time': start_time,
                'end_time': time_range[1],
                'booked_count': booked_count,
                'available_spots': max(0, available_spots),
                'is_full': available_spots <= 0,
                'percentage_full': round((booked_count / 6) * 100, 1)
            })

        cursor.close()
        conn.close()

        return jsonify({
            'date': date,
            'user_type': user_type,
            'slots': availability,
            'total_slots': len(availability)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/book', methods=['POST'])
def book_slot():
    """Book a time slot for a user"""
    try:
        data = request.get_json()
        date = data.get('date')
        time_slot = data.get('time_slot')
        member_id = data.get('member_id')
        
        if not all([date, time_slot, member_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Extract start time from time slot (e.g., "09:00 - 10:00" -> "09:00")
        start_time = time_slot.split(' - ')[0]

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Check if slot is still available
        cursor.execute("""
            SELECT COUNT(*) as booked_count
            FROM booking
            WHERE BOOKING_Date = %s AND BOOKING_Time = %s AND BOOKING_Status != 'Cancelled'
        """, (date, start_time))
        
        booked_count = cursor.fetchone()[0]
        
        if booked_count >= 6:
            cursor.close()
            conn.close()
            return jsonify({'error': 'This slot is already full'}), 400

        # Check if user already has a booking for this date
        cursor.execute("""
            SELECT COUNT(*) as user_bookings
            FROM booking
            WHERE BOOKING_Date = %s AND MEMBER_ID = %s AND BOOKING_Status != 'Cancelled'
        """, (date, member_id))
        
        user_bookings = cursor.fetchone()[0]
        
        if user_bookings >= 2:
            cursor.close()
            conn.close()
            return jsonify({'error': 'You can only book up to 2 slots per day'}), 400

        # Create the booking with shorter reference format
        booking_ref = generate_booking_ref()
        
        # Use session ID 9999 for all bookings
        cursor.execute("""
            INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            booking_ref,
            member_id,
            9999,  # Use session ID 9999
            date,
            start_time,
            'Confirmed'
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'message': 'Booking successful',
            'booking_ref': booking_ref,
            'date': date,
            'time_slot': time_slot
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_booking_ref():
    """Generate a shorter booking reference compatible with the database"""
    # Format: BK + YYMMDD + 3-digit sequence
    now = datetime.now()
    date_part = now.strftime('%y%m%d')  # YYMMDD format
    time_part = now.strftime('%H%M')    # HHMM format
    return f"BK{date_part}{time_part}"

def generate_available_slots(date, user_type):
    """Generate available time slots based on user type and date"""
    from datetime import datetime
    
    # Parse the date to get day of week
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%A')
    
    # Define time ranges based on user type and day
    staff_hours = {
        'Monday': [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
        'Tuesday': [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
        'Wednesday': [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
        'Thursday': [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
        'Friday': [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
        'Saturday': [["07:00", "13:00"]],
    }
    
    student_hours = {
        'Monday': [["08:00", "22:00"]],
        'Tuesday': [["08:00", "22:00"]],
        'Wednesday': [["08:00", "22:00"]],
        'Thursday': [["08:00", "22:00"]],
        'Friday': [["08:00", "22:00"]],
        'Saturday': [["08:00", "18:00"]],
    }
    
    ranges = staff_hours[day_of_week] if user_type == 'staff' else student_hours[day_of_week]
    
    if not ranges:
        return []
    
    slots = []
    for start, end in ranges:
        start_minutes = int(start.split(':')[0]) * 60 + int(start.split(':')[1])
        end_minutes = int(end.split(':')[0]) * 60 + int(end.split(':')[1])
        
        current = start_minutes
        while current + 60 <= end_minutes:
            start_time = f"{current // 60:02d}:{current % 60:02d}"
            end_time = f"{(current + 60) // 60:02d}:{(current + 60) % 60:02d}"
            slots.append(f"{start_time} - {end_time}")
            current += 60
    
    return slots
