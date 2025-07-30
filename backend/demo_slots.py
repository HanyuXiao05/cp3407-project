#!/usr/bin/env python3
"""
Demo script to populate the database with sample booking data
for testing real-time slot availability
"""

import pymysql
from datetime import datetime, timedelta
from config import db_config

def create_sample_bookings():
    """Create sample bookings for testing real-time availability"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Get today's date and next few days
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)
        
        # Sample booking data
        sample_bookings = [
            # Today's bookings
            ('BK20241201090001', 'M001', 1, today, '09:00', 'Confirmed'),
            ('BK20241201090002', 'M002', 1, today, '09:00', 'Confirmed'),
            ('BK20241201090003', 'M003', 1, today, '09:00', 'Confirmed'),
            ('BK20241201090004', 'M004', 1, today, '09:00', 'Confirmed'),
            ('BK20241201090005', 'M005', 1, today, '09:00', 'Confirmed'),
            ('BK20241201090006', 'M006', 1, today, '09:00', 'Confirmed'),  # Full slot
            
            ('BK20241201100001', 'M007', 1, today, '10:00', 'Confirmed'),
            ('BK20241201100002', 'M008', 1, today, '10:00', 'Confirmed'),
            ('BK20241201100003', 'M009', 1, today, '10:00', 'Confirmed'),
            
            ('BK20241201110001', 'M010', 1, today, '11:00', 'Confirmed'),
            ('BK20241201110002', 'M011', 1, today, '11:00', 'Confirmed'),
            ('BK20241201110003', 'M012', 1, today, '11:00', 'Confirmed'),
            ('BK20241201110004', 'M013', 1, today, '11:00', 'Confirmed'),
            ('BK20241201110005', 'M014', 1, today, '11:00', 'Confirmed'),
            
            # Tomorrow's bookings
            ('BK20241202080001', 'M015', 1, tomorrow, '08:00', 'Confirmed'),
            ('BK20241202080002', 'M016', 1, tomorrow, '08:00', 'Confirmed'),
            
            ('BK20241202090001', 'M017', 1, tomorrow, '09:00', 'Confirmed'),
            ('BK20241202090002', 'M018', 1, tomorrow, '09:00', 'Confirmed'),
            ('BK20241202090003', 'M019', 1, tomorrow, '09:00', 'Confirmed'),
            ('BK20241202090004', 'M020', 1, tomorrow, '09:00', 'Confirmed'),
            ('BK20241202090005', 'M021', 1, tomorrow, '09:00', 'Confirmed'),
            ('BK20241202090006', 'M022', 1, tomorrow, '09:00', 'Confirmed'),  # Full slot
            
            # Day after tomorrow - mostly empty
            ('BK20241203080001', 'M023', 1, day_after, '08:00', 'Confirmed'),
        ]
        
        # Clear existing demo bookings (optional)
        cursor.execute("DELETE FROM booking WHERE BOOKING_Ref LIKE 'BK2024%'")
        
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
        
        cursor.execute("DELETE FROM booking WHERE BOOKING_Ref LIKE 'BK2024%'")
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