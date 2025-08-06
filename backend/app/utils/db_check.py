# app/utils/db_check.py
import pymysql
from config import db_config

def test_database_connection():
    """Test direct database connection using pymysql"""
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        tables = ['member', 'session', 'membership_type', 'membership', 'booking', 'payment']
        table_counts = {}

        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cursor.fetchone()[0]
            except Exception as e:
                table_counts[table] = f"Error: {e}"

        cursor.close()
        conn.close()

        return {
            'status': 'success',
            'message': 'Database connection successful',
            'table_counts': table_counts
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Database connection failed: {str(e)}',
            'table_counts': {}
        }
