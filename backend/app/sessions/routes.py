# app/sessions/routes.py
from flask import Blueprint, jsonify, request
import pymysql
import random
import time
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

def convert_member_id(member_id):
    """Convert string member ID to integer member ID"""
    # Mapping for demo purposes - in real app, this would come from authentication
    member_mapping = {
        'M001': 2303,  # Tyler Pope
        'M002': 2304,  # Erika Bowen
        'M003': 2305,  # Vera Alvarado
        'M004': 2306,  # Aria Williams
        'M005': 2307,  # Ella Brown
    }
    
    # If it's already an integer, return as is
    if isinstance(member_id, int):
        return member_id
    
    # If it's a string, try to convert using mapping
    if isinstance(member_id, str):
        if member_id in member_mapping:
            return member_mapping[member_id]
        else:
            # Try to convert directly to int if it's a numeric string
            try:
                return int(member_id)
            except ValueError:
                raise ValueError(f"Invalid member ID: {member_id}")
    
    raise ValueError(f"Invalid member ID type: {type(member_id)}")

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

        # Convert string member ID to integer
        try:
            member_id_int = convert_member_id(member_id)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

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
        """, (date, member_id_int))
        
        user_bookings = cursor.fetchone()[0]
        
        if user_bookings >= 2:
            cursor.close()
            conn.close()
            return jsonify({'error': 'You can only book up to 2 slots per day'}), 400

        # Find the appropriate session ID based on date and time
        cursor.execute("""
            SELECT SESSION_ID FROM session 
            WHERE SESSION_Date = %s AND SESSION_Time = %s
        """, (date, start_time))
        
        session_result = cursor.fetchone()
        if not session_result:
            # Get available dates to help the user
            cursor.execute("""
                SELECT DISTINCT SESSION_Date FROM session 
                ORDER BY SESSION_Date 
                LIMIT 5
            """)
            available_dates = [row[0].strftime('%Y-%m-%d') for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            return jsonify({
                'error': f'No session found for date {date} and time {start_time}',
                'available_dates': available_dates,
                'message': 'Please select a date from the available sessions'
            }), 400
        
        session_id = session_result[0]
        
        # Create the booking with unique reference (BK + timestamp)
        max_attempts = 10
        for attempt in range(max_attempts):
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            booking_ref = f"BK{timestamp}"
            
            try:
                cursor.execute("""
                    INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    booking_ref,
                    member_id_int,
                    session_id,
                    date,
                    start_time,
                    'Booked'
                ))
                break  # Success, exit the retry loop
            except pymysql.err.IntegrityError as e:
                if "Duplicate entry" in str(e) and attempt < max_attempts - 1:
                    # Add a longer delay to ensure different timestamp
                    time.sleep(1)
                    continue  # Try again with a new timestamp
                else:
                    raise  # Re-raise the error if max attempts reached

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

@sessions_bp.route('/book-multiple', methods=['POST'])
def book_multiple_slots():
    """Book multiple time slots for a user in a single transaction"""
    try:
        data = request.get_json()
        date = data.get('date')
        time_slots = data.get('time_slots', [])
        member_id = data.get('member_id')
        
        if not all([date, time_slots, member_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        if len(time_slots) > 2:
            return jsonify({'error': 'You can only book up to 2 slots per day'}), 400

        # Convert string member ID to integer
        try:
            member_id_int = convert_member_id(member_id)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Check if user already has any bookings for this date
        cursor.execute("""
            SELECT COUNT(*) as user_bookings
            FROM booking
            WHERE BOOKING_Date = %s AND MEMBER_ID = %s AND BOOKING_Status != 'Cancelled'
        """, (date, member_id_int))
        
        existing_bookings = cursor.fetchone()[0]
        
        if existing_bookings + len(time_slots) > 2:
            cursor.close()
            conn.close()
            return jsonify({'error': f'You can only book up to 2 slots per day. You already have {existing_bookings} booking(s)'}), 400

        booking_results = []
        
        for time_slot in time_slots:
            # Extract start time from time slot
            start_time = time_slot.split(' - ')[0]
            
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
                return jsonify({'error': f'Slot {time_slot} is already full'}), 400

            # Find the appropriate session ID
            cursor.execute("""
                SELECT SESSION_ID FROM session 
                WHERE SESSION_Date = %s AND SESSION_Time = %s
            """, (date, start_time))
            
            session_result = cursor.fetchone()
            if not session_result:
                cursor.close()
                conn.close()
                return jsonify({'error': f'No session found for date {date} and time {start_time}'}), 400
            
            session_id = session_result[0]
            
            # Create the booking with unique reference (BK + timestamp)
            max_attempts = 10
            for attempt in range(max_attempts):
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                booking_ref = f"BK{timestamp}"
                
                try:
                    cursor.execute("""
                        INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        booking_ref,
                        member_id_int,
                        session_id,
                        date,
                        start_time,
                        'Booked'
                    ))
                    booking_results.append({
                        'time_slot': time_slot,
                        'booking_ref': booking_ref
                    })
                    break
                except pymysql.err.IntegrityError as e:
                    if "Duplicate entry" in str(e) and attempt < max_attempts - 1:
                        # Add a longer delay to ensure different timestamp
                        time.sleep(1)
                        continue  # Try again with a new timestamp
                    else:
                        raise  # Re-raise the error if max attempts reached

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'message': 'Multiple bookings successful',
            'bookings': booking_results,
            'date': date
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/capacity', methods=['GET'])
def get_gym_capacity():
    """Get real-time gym capacity information"""
    try:
        date = request.args.get('date')
        
        if not date:
            return jsonify({'error': 'Date parameter is required'}), 400

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Get total bookings for the specified date
        cursor.execute("""
            SELECT COUNT(*) as total_bookings
            FROM booking b
            WHERE b.BOOKING_Date = %s AND b.BOOKING_Status != 'Cancelled'
        """, (date,))
        
        total_bookings = cursor.fetchone()[0]

        # Get bookings by time slot for detailed capacity
        cursor.execute("""
            SELECT b.BOOKING_Time, COUNT(*) as booked_count
            FROM booking b
            WHERE b.BOOKING_Date = %s AND b.BOOKING_Status != 'Cancelled'
            GROUP BY b.BOOKING_Time
            ORDER BY b.BOOKING_Time
        """, (date,))
        
        time_slot_capacity = []
        for row in cursor.fetchall():
            time_slot_capacity.append({
                'time': str(row[0]),
                'booked_count': row[1],
                'available_spots': 6 - row[1],
                'percentage_full': round((row[1] / 6) * 100, 1)
            })

        # Calculate overall gym capacity
        total_slots = len(time_slot_capacity) * 6  # 6 people per slot
        total_available = total_slots - total_bookings
        overall_percentage = round((total_bookings / total_slots) * 100, 1) if total_slots > 0 else 0

        cursor.close()
        conn.close()

        return jsonify({
            'date': date,
            'total_bookings': total_bookings,
            'total_available_spots': total_available,
            'overall_percentage_full': overall_percentage,
            'time_slot_capacity': time_slot_capacity,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/admin/members', methods=['GET'])
def get_all_members():
    """Get all member information for admin dashboard"""
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                m.MEMBER_ID,
                m.MEMBER_Name,
                m.MEMBER_Email,
                mt.MEMBERSHIP_TYPE_Name,
                m.MEMBER_JoinDate,
                m.MEMBER_Status,
                COUNT(b.BOOKING_Ref) as total_bookings,
                MAX(b.BOOKING_Date) as last_booking
            FROM member m
            LEFT JOIN membership_type mt ON m.MEMBERSHIP_TYPE_ID = mt.MEMBERSHIP_TYPE_ID
            LEFT JOIN booking b ON m.MEMBER_ID = b.MEMBER_ID AND b.BOOKING_Status != 'Cancelled'
            GROUP BY m.MEMBER_ID, m.MEMBER_Name, m.MEMBER_Email, mt.MEMBERSHIP_TYPE_Name, m.MEMBER_JoinDate, m.MEMBER_Status
            ORDER BY m.MEMBER_ID
        """)
        
        members = []
        for row in cursor.fetchall():
            members.append({
                'member_id': row[0],
                'name': row[1],
                'email': row[2],
                'membership_type': row[3],
                'join_date': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'status': row[5],
                'total_bookings': row[6] or 0,
                'last_booking': row[7].strftime('%Y-%m-%d') if row[7] else None
            })

        cursor.close()
        conn.close()

        return jsonify({'members': members})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/admin/bookings', methods=['GET'])
def get_all_bookings():
    """Get all booking information for admin dashboard"""
    try:
        date = request.args.get('date')
        status_filter = request.args.get('status', '')
        
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        query = """
            SELECT 
                b.BOOKING_Ref,
                b.MEMBER_ID,
                m.MEMBER_Name,
                b.BOOKING_Date,
                b.BOOKING_Time,
                b.BOOKING_Status,
                b.BOOKING_CheckIn,
                b.BOOKING_CheckOut
            FROM booking b
            JOIN member m ON b.MEMBER_ID = m.MEMBER_ID
            WHERE 1=1
        """
        
        params = []
        
        if date:
            query += " AND b.BOOKING_Date = %s"
            params.append(date)
            
        if status_filter:
            query += " AND b.BOOKING_Status = %s"
            params.append(status_filter)
            
        query += " ORDER BY b.BOOKING_Date DESC, b.BOOKING_Time ASC"
        
        cursor.execute(query, params)
        
        bookings = []
        for row in cursor.fetchall():
            # Format time range
            start_time = str(row[4])
            end_time = (datetime.strptime(start_time, '%H:%M:%S') + timedelta(hours=1)).strftime('%H:%M:%S')
            time_range = f"{start_time} - {end_time}"
            
            bookings.append({
                'booking_ref': row[0],
                'member_id': row[1],
                'member_name': row[2],
                'date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'time': time_range,
                'status': row[5],
                'check_in': row[6].strftime('%Y-%m-%d %H:%M') if row[6] else None,
                'check_out': row[7].strftime('%Y-%m-%d %H:%M') if row[7] else None
            })

        cursor.close()
        conn.close()

        return jsonify({'bookings': bookings})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Get today's statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_bookings,
                SUM(CASE WHEN BOOKING_Status = 'Attended' THEN 1 ELSE 0 END) as attended,
                SUM(CASE WHEN BOOKING_Status = 'No-Show' THEN 1 ELSE 0 END) as no_show,
                SUM(CASE WHEN BOOKING_Status = 'Booked' THEN 1 ELSE 0 END) as active
            FROM booking
            WHERE BOOKING_Date = %s
        """, (date,))
        
        stats = cursor.fetchone()
        
        # Calculate attendance rate
        total = stats[0] or 0
        attended = stats[1] or 0
        attendance_rate = round((attended / total) * 100, 1) if total > 0 else 0

        cursor.close()
        conn.close()

        return jsonify({
            'date': date,
            'total_bookings': total,
            'attended': attended,
            'no_show': stats[2] or 0,
            'active': stats[3] or 0,
            'attendance_rate': attendance_rate
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
