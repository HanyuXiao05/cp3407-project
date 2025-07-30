#!/usr/bin/env python3
"""
Script to fix the database schema for booking reference length issue
"""

import pymysql
from config import db_config

def fix_database_schema():
    """Fix the database schema to accommodate longer booking references"""
    
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("🔧 Fixing database schema...")
        
        # Alter the BOOKING_Ref column to allow longer strings
        print("📝 Updating BOOKING_Ref column length...")
        cursor.execute("""
            ALTER TABLE booking MODIFY COLUMN BOOKING_Ref VARCHAR(20) NOT NULL
        """)
        
        # Update the BOOKING_Status enum to include 'Confirmed' status
        print("📝 Updating BOOKING_Status enum...")
        cursor.execute("""
            ALTER TABLE booking MODIFY COLUMN BOOKING_Status 
            ENUM('Booked', 'Deleted', 'Attended', 'No-Show', 'Confirmed', 'Cancelled') NOT NULL
        """)
        
        conn.commit()
        
        # Verify the changes
        print("✅ Verifying changes...")
        cursor.execute("DESCRIBE booking")
        columns = cursor.fetchall()
        
        print("\n📊 Updated booking table structure:")
        for column in columns:
            print(f"  {column[0]}: {column[1]}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database schema fixed successfully!")
        print("🎯 You can now use the session booking system without errors")
        
    except Exception as e:
        print(f"❌ Error fixing database schema: {e}")
        print("💡 Make sure your MySQL server is running and accessible")

if __name__ == "__main__":
    fix_database_schema() 