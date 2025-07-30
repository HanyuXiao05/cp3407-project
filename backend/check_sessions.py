#!/usr/bin/env python3
"""
Script to check available session IDs in the database
"""

import pymysql
from config import db_config

def check_sessions():
    """Check available session IDs"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("🔍 Checking available sessions...")
        
        # Check if session table has any data
        cursor.execute("SELECT COUNT(*) FROM session")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("⚠️  No sessions found in the database!")
            print("💡 You need to populate the session table first")
            return
        
        # Get all session IDs
        cursor.execute("SELECT SESSION_ID, SESSION_Date, SESSION_Time FROM session LIMIT 10")
        sessions = cursor.fetchall()
        
        print(f"\n📊 Found {len(sessions)} sessions:")
        for session in sessions:
            print(f"  Session ID: {session[0]}, Date: {session[1]}, Time: {session[2]}")
        
        # Get the minimum session ID
        cursor.execute("SELECT MIN(SESSION_ID) FROM session")
        min_id = cursor.fetchone()[0]
        
        print(f"\n🎯 Minimum Session ID: {min_id}")
        print("💡 Use this ID for demo bookings")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking sessions: {e}")

if __name__ == "__main__":
    check_sessions() 