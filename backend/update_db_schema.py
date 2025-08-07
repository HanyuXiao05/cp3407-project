#!/usr/bin/env python3
"""
Script to update the database schema to increase BOOKING_Ref column length
"""

import pymysql
from config import db_config

def update_booking_ref_column():
    """Update the BOOKING_Ref column to varchar(20)"""
    try:
        # Connect to database
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("Updating BOOKING_Ref column to varchar(20)...")
        
        # Update the column
        cursor.execute("""
            ALTER TABLE `booking` 
            MODIFY COLUMN `BOOKING_Ref` varchar(20) NOT NULL
        """)
        
        conn.commit()
        print("✅ Successfully updated BOOKING_Ref column to varchar(20)")
        
        # Verify the change
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'booking' AND COLUMN_NAME = 'BOOKING_Ref'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Column verified: {result[0]} - {result[1]}({result[2]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Database Schema Update Script")
    print("=" * 40)
    
    success = update_booking_ref_column()
    
    if success:
        print("\n✅ Database schema updated successfully!")
        print("The booking system can now generate 16-character references.")
    else:
        print("\n❌ Failed to update database schema.")
        print("Please check the error message above.") 