#!/usr/bin/env python3
"""
Demo script to populate the database with sample booking data
for testing real-time slot availability
"""

import pymysql
from datetime import datetime, timedelta
from config import db_config

def generate_booking_ref(sequence):
    """Generate a shorter booking reference compatible with the database"""
    # Format: BK + YYMMDD + 3-digit sequence
    now = datetime.now()
    date_part = now.strftime('%y%m%d')  # YYMMDD format
    return f"BK{date_part}{sequence:03d}"

def create_sample_bookings():
    """Create sample bookings for testing real-time availability"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Get today's date and next few days
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)
        
        # Sample booking data with integer member IDs and session ID 9999
        sample_bookings = [
            # Today's bookings
            (generate_booking_ref(1), 2304, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(2), 2305, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(3), 2306, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(4), 2307, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(5), 2308, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(6), 2309, 9999, today, '09:00', 'Confirmed'),  # Full slot
            
            (generate_booking_ref(7), 2310, 9999, today, '10:00', 'Confirmed'),
            (generate_booking_ref(8), 2311, 9999, today, '10:00', 'Confirmed'),
            (generate_booking_ref(9), 2312, 9999, today, '10:00', 'Confirmed'),
            
            (generate_booking_ref(10), 2313, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(11), 2314, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(12), 2315, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(13), 2316, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(14), 2317, 9999, today, '11:00', 'Confirmed'),
            
            # Tomorrow's bookings
            (generate_booking_ref(15), 2318, 9999, tomorrow, '08:00', 'Confirmed'),
            (generate_booking_ref(16), 2319, 9999, tomorrow, '08:00', 'Confirmed'),
            
            (generate_booking_ref(17), 2320, 9999, tomorrow, '09:00', 'Confirmed'),
            (generate_booking_ref(18), 2321, 9999, tomorrow, '09:00', 'Confirmed'),
            (generate_booking_ref(19), 2322, 9999, tomorrow, '09:00', 'Confirmed'),
            (generate_booking_ref(20), 2323, 9999, tomorrow, '09:00', 'Confirmed'),
            (generate_booking_ref(21), 2324, 9999, tomorrow, '09:00', 'Confirmed'),
            (generate_booking_ref(22), 2325, 9999, tomorrow, '09:00', 'Confirmed'),  # Full slot
            
            # Day after tomorrow - mostly empty
            (generate_booking_ref(23), 2326, 9999, day_after, '08:00', 'Confirmed'),
        ]
        
        # Clear existing demo bookings (optional)
        cursor.execute("DELETE FROM booking WHERE BOOKING_Ref LIKE 'BK%' AND BOOKING_Ref NOT LIKE 'GYM%'")
        
        # Insert sample bookings
        for booking in sample_bookings:
            cursor.execute("""
                INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, booking)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Sample bookings created successfully!")
        print(f"📅 Created bookings for: {today}, {tomorrow}, {day_after}")
        print("🎯 You can now test the real-time availability system")
        
    except Exception as e:
        print(f"❌ Error creating sample bookings: {e}")

def clear_sample_bookings():
    """Clear all demo bookings"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM booking WHERE BOOKING_Ref LIKE 'BK%' AND BOOKING_Ref NOT LIKE 'GYM%'")
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Sample bookings cleared successfully!")
        
    except Exception as e:
        print(f"❌ Error clearing sample bookings: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_sample_bookings()
    else:
        create_sample_bookings() 