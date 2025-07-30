#!/usr/bin/env python3
"""
Script to create a simple session for testing
"""

import pymysql
from datetime import datetime, timedelta
from config import db_config

def create_test_session():
    """Create a simple test session"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("🔧 Creating test session...")
        
        # Create a simple session
        session_id = 9999  # Use a high number to avoid conflicts
        session_date = datetime.now().date()
        session_time = '09:00:00'
        session_capacity = 6
        
        cursor.execute("""
            INSERT INTO session (SESSION_ID, SESSION_Date, SESSION_Time, SESSION_Capacity)
            VALUES (%s, %s, %s, %s)
        """, (session_id, session_date, session_time, session_capacity))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Test session created successfully!")
        print(f"📅 Session ID: {session_id}")
        print("🎯 You can now use this session ID for bookings")
        
    except Exception as e:
        print(f"❌ Error creating test session: {e}")

if __name__ == "__main__":
    create_test_session() 