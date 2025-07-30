#!/usr/bin/env python3
"""
Script to check current bookings and slot availability
"""

import pymysql
from datetime import datetime
from config import db_config

def check_bookings():
    """Check current bookings and slot availability"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("🔍 Checking current bookings...")
        
        # Get today's date
        today = datetime.now().date()
        
        # Get all bookings for today
        cursor.execute("""
            SELECT BOOKING_Time, COUNT(*) as booked_count
            FROM booking 
            WHERE BOOKING_Date = %s AND BOOKING_Status != 'Cancelled'
            GROUP BY BOOKING_Time
            ORDER BY BOOKING_Time
        """, (today,))
        
        bookings = cursor.fetchall()
        
        print(f"\n📅 Bookings for {today}:")
        for booking in bookings:
            time_slot = booking[0]
            count = booking[1]
            available = 6 - count
            status = "🟢 Available" if available > 0 else "🔴 Full"
            print(f"  {time_slot}: {count}/6 booked ({available} spots left) {status}")
        
        # Get tomorrow's bookings
        tomorrow = today.replace(day=today.day + 1)
        cursor.execute("""
            SELECT BOOKING_Time, COUNT(*) as booked_count
            FROM booking 
            WHERE BOOKING_Date = %s AND BOOKING_Status != 'Cancelled'
            GROUP BY BOOKING_Time
            ORDER BY BOOKING_Time
        """, (tomorrow,))
        
        tomorrow_bookings = cursor.fetchall()
        
        print(f"\n📅 Bookings for {tomorrow}:")
        for booking in tomorrow_bookings:
            time_slot = booking[0]
            count = booking[1]
            available = 6 - count
            status = "🟢 Available" if available > 0 else "🔴 Full"
            print(f"  {time_slot}: {count}/6 booked ({available} spots left) {status}")
        
        cursor.close()
        conn.close()
        
        print("\n💡 Tips:")
        print("  - Try booking slots that show 'Available' status")
        print("  - Use the refresh button to get latest availability")
        print("  - Try different dates (today, tomorrow, day after)")
        
    except Exception as e:
        print(f"❌ Error checking bookings: {e}")

if __name__ == "__main__":
    check_bookings() 