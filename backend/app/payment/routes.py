from flask import Blueprint, jsonify, request
import pymysql
from config import db_config

payment_bp = Blueprint('payment', __name__)

# GET all payments
@payment_bp.route('/', methods=['GET'])
def get_payments():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT PAYMENT_ID, MEMBERSHIP_ID, PAYMENT_Date, PAYMENT_TotalFee, 
                   PAYMENT_Type, PAYMENT_RcptNum, PAYMENT_RcptVerifiedBy
            FROM payment
            ORDER BY PAYMENT_Date DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        payments = []
        for row in data:
            payments.append({
                'payment_id': row[0],
                'membership_id': row[1],
                'payment_date': row[2].strftime('%Y-%m-%d') if row[2] else None,
                'total_fee': float(row[3]),
                'payment_type': row[4],
                'receipt_number': row[5],
                'verified_by': row[6]
            })

        return jsonify({'payments': payments, 'count': len(payments)})
    except Exception as e:
        return jsonify({'error': str(e), 'payments': [], 'count': 0}), 500

# GET one payment by ID
@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT PAYMENT_ID, MEMBERSHIP_ID, PAYMENT_Date, PAYMENT_TotalFee, 
                   PAYMENT_Type, PAYMENT_RcptNum, PAYMENT_RcptVerifiedBy
            FROM payment
            WHERE PAYMENT_ID = %s
        """, (payment_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return jsonify({
                'payment_id': row[0],
                'membership_id': row[1],
                'payment_date': row[2].strftime('%Y-%m-%d') if row[2] else None,
                'total_fee': float(row[3]),
                'payment_type': row[4],
                'receipt_number': row[5],
                'verified_by': row[6]
            })
        else:
            return jsonify({'error': 'Payment not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST new payment
@payment_bp.route('/', methods=['POST'])
def create_payment():
    try:
        data = request.get_json()
        required_fields = ['membership_id', 'payment_date', 'total_fee', 'payment_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO payment (MEMBERSHIP_ID, PAYMENT_Date, PAYMENT_TotalFee, 
                                 PAYMENT_Type, PAYMENT_RcptNum, PAYMENT_RcptVerifiedBy)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['membership_id'],
            data['payment_date'],
            data['total_fee'],
            data['payment_type'],
            data.get('receipt_number'),
            data.get('verified_by')
        ))

        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({'message': 'Payment recorded successfully', 'payment_id': new_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT update existing payment
@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    try:
        data = request.get_json()
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE payment
            SET MEMBERSHIP_ID = %s,
                PAYMENT_Date = %s,
                PAYMENT_TotalFee = %s,
                PAYMENT_Type = %s,
                PAYMENT_RcptNum = %s,
                PAYMENT_RcptVerifiedBy = %s
            WHERE PAYMENT_ID = %s
        """, (
            data.get('membership_id'),
            data.get('payment_date'),
            data.get('total_fee'),
            data.get('payment_type'),
            data.get('receipt_number'),
            data.get('verified_by'),
            payment_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Payment updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE a payment
@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM payment WHERE PAYMENT_ID = %s", (payment_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Payment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
