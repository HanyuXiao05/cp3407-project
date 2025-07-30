#!/usr/bin/env python3
"""
Script to create a few test bookings to demonstrate real-time availability
"""

import pymysql
from datetime import datetime, timedelta
from config import db_config

def generate_booking_ref(sequence):
    """Generate a shorter booking reference compatible with the database"""
    now = datetime.now()
    date_part = now.strftime('%y%m%d')
    return f"BK{date_part}{sequence:03d}"

def create_test_bookings():
    """Create a few test bookings to demonstrate availability"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Get today's date
        today = datetime.now().date()
        
        # Create just a few bookings to show partial availability
        test_bookings = [
            # Today - 09:00 slot (3/6 booked - available)
            (generate_booking_ref(1), 2304, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(2), 2305, 9999, today, '09:00', 'Confirmed'),
            (generate_booking_ref(3), 2306, 9999, today, '09:00', 'Confirmed'),
            
            # Today - 10:00 slot (5/6 booked - limited)
            (generate_booking_ref(4), 2307, 9999, today, '10:00', 'Confirmed'),
            (generate_booking_ref(5), 2308, 9999, today, '10:00', 'Confirmed'),
            (generate_booking_ref(6), 2309, 9999, today, '10:00', 'Confirmed'),
            (generate_booking_ref(7), 2310, 9999, today, '10:00', 'Confirmed'),
            (generate_booking_ref(8), 2311, 9999, today, '10:00', 'Confirmed'),
            
            # Today - 11:00 slot (6/6 booked - full)
            (generate_booking_ref(9), 2312, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(10), 2313, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(11), 2314, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(12), 2315, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(13), 2316, 9999, today, '11:00', 'Confirmed'),
            (generate_booking_ref(14), 2317, 9999, today, '11:00', 'Confirmed'),
        ]
        
        # Insert test bookings
        for booking in test_bookings:
            cursor.execute("""
                INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, booking)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Test bookings created successfully!")
        print(f"📅 Created test bookings for {today}")
        print("\n🎯 Test Scenarios:")
        print("  🟢 09:00 slot: 3/6 booked (3 spots available)")
        print("  🟡 10:00 slot: 5/6 booked (1 spot left)")
        print("  🔴 11:00 slot: 6/6 booked (full)")
        print("  🟢 Other slots: Available")
        print("\n💡 Now you can test the real-time availability system!")
        
    except Exception as e:
        print(f"❌ Error creating test bookings: {e}")

if __name__ == "__main__":
    create_test_bookings() 