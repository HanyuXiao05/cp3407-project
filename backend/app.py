from app.payment.routes import payment_bp
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pymysql
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Database connection configuration
db_config = {
    'host': '43.160.205.48',
    'port': 3306,
    'user': 'root',
    'password': 'CP3407',
    'database': 'jcu_gym_ms_db'
}

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
CORS(app)


# SQLAlchemy Member model for authentication
class Member(db.Model):
    __tablename__ = 'member'
    
    MEMBER_ID = db.Column(db.Integer, primary_key=True)
    MEMBER_Title = db.Column(db.String(10), nullable=False)
    MEMBER_Name = db.Column(db.String(45), nullable=False)
    MEMBER_Gender = db.Column(db.String(10), nullable=False)
    MEMBER_DOB = db.Column(db.Date, nullable=False)
    MEMBER_Phone = db.Column(db.String(20), nullable=False)
    MEMBER_Email = db.Column(db.String(100), nullable=False, unique=True)
    MEMBER_EmgContactName = db.Column(db.String(45))
    MEMBER_EmgContactPhone = db.Column(db.String(20))
    MEMBER_PwdHash = db.Column(db.String(512), nullable=False)
    MEMBER_Type = db.Column(db.String(10), nullable=False)
    MEMBER_JCID = db.Column(db.BigInteger)
    MEMBER_JCCompUsrnme = db.Column(db.String(100))

    
    # Flask-Login required methods
    def get_id(self):
        return str(self.MEMBER_ID)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# Auth Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        required_fields = ['title', 'name', 'gender', 'dob', 'phone', 'email', 
                           'password', 'member_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        if Member.query.filter_by(MEMBER_Email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        jc_id = data.get('jc_id')
        jc_username = data.get('jc_username')

        new_member = Member(
            MEMBER_Title=data['title'],
            MEMBER_Name=data['name'],
            MEMBER_Gender=data['gender'],
            MEMBER_DOB=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            MEMBER_Phone=data['phone'],
            MEMBER_Email=data['email'],
            MEMBER_PwdHash=generate_password_hash(data['password']),
            MEMBER_Type=data['member_type'],
            MEMBER_JCID=jc_id,
            MEMBER_JCCompUsrnme=jc_username
        )

        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member registered successfully', 'member_id': new_member.MEMBER_ID}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing email or password'}), 400
        
        member = Member.query.filter_by(MEMBER_Email=data['email']).first()
        
        if not member or not check_password_hash(member.MEMBER_PwdHash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        login_user(member)
        
        return jsonify({
            'message': 'Login successful',
            'member': {
                'id': member.MEMBER_ID,
                'name': member.MEMBER_Name,
                'email': member.MEMBER_Email,
                'type': member.MEMBER_Type
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        'member': {
            'id': current_user.MEMBER_ID,
            'title': current_user.MEMBER_Title,
            'name': current_user.MEMBER_Name,
            'gender': current_user.MEMBER_Gender,
            'dob': current_user.MEMBER_DOB.strftime('%Y-%m-%d'),
            'phone': current_user.MEMBER_Phone,
            'email': current_user.MEMBER_Email,
            'type': current_user.MEMBER_Type,
            'emergency_contact_name': current_user.MEMBER_EmgContactName,
            'emergency_contact_phone': current_user.MEMBER_EmgContactPhone
        }
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        data = request.get_json()
        
        # 不允许更新的字段
        protected_fields = ['MEMBER_ID', 'MEMBER_Email', 'MEMBER_PwdHash', 'MEMBER_Type']
        
        for key, value in data.items():
            if key not in protected_fields:
                if key == 'dob':
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(current_user, f'MEMBER_{key}', value)
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Register auth blueprint
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix="/api/payment")

# Basic route for testing
@app.route('/')
def index():
    return jsonify({
        'message': 'JCU Gym Management System API',
        'status': 'running',
        'endpoints': {
            'auth': '/api/auth',
            'booking': '/api/booking',
            'payment': '/api/payment',
            'members': '/api/members',
            'sessions': '/api/sessions',
            'memberships': '/api/memberships',
            'test': '/api/test-db'
        }
    })

@app.route('/api')
def api_index():
    return jsonify({
        'message': 'JCU Gym Management System API Documentation',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'register': {
                    'url': '/api/auth/register',
                    'method': 'POST',
                    'description': 'Register new user'
                },
                'login': {
                    'url': '/api/auth/login',
                    'method': 'POST',
                    'description': 'User login'
                },
                'logout': {
                    'url': '/api/auth/logout',
                    'method': 'POST',
                    'description': 'User logout'
                },
                'profile': {
                    'url': '/api/auth/profile',
                    'methods': ['GET', 'PUT'],
                    'description': 'Get or update user profile'
                }
            },
            'members': {
                'all_members': {
                    'url': '/api/members',
                    'method': 'GET',
                    'description': 'Get all members'
                },
                'single_member': {
                    'url': '/api/members/<member_id>',
                    'method': 'GET',
                    'description': 'Get specific member information'
                },
                'search_members': {
                    'url': '/api/members/search',
                    'method': 'GET',
                    'description': 'Search members (supports ?q=name&type=Student/Staff)'
                }
            },
            'sessions': {
                'all_sessions': {
                    'url': '/api/sessions',
                    'method': 'GET',
                    'description': 'Get all sessions'
                },
                'single_session': {
                    'url': '/api/sessions/<session_id>',
                    'method': 'GET',
                    'description': 'Get specific session information'
                }
            },
            'memberships': {
                'all_memberships': {
                    'url': '/api/memberships',
                    'method': 'GET',
                    'description': 'Get all memberships'
                },
                'membership_types': {
                    'url': '/api/membership-types',
                    'method': 'GET',
                    'description': 'Get membership types list'
                }
            },
            'bookings': {
                'all_bookings': {
                    'url': '/api/bookings',
                    'method': 'GET',
                    'description': 'Get all bookings'
                },
                'single_booking': {
                    'url': '/api/bookings/<booking_ref>',
                    'method': 'GET',
                    'description': 'Get specific booking information'
                }
            },
            'payments': {
                'all_payments': {
                    'url': '/api/payments',
                    'method': 'GET',
                    'description': 'Get all payments'
                },
                'single_payment': {
                    'url': '/api/payments/<payment_id>',
                    'method': 'GET',
                    'description': 'Get specific payment information'
                }
            }
        }
    })

# Try to register other blueprints
try:
    from app.booking.routes import booking_bp
    from app.payment.routes import payment_bp
    
    print("Additional blueprints registered successfully")
except ImportError as e:
    print(f"Additional blueprint import failed: {e}")
    print("Auth blueprint is available, others using direct routes")

def test_database_connection():
    """Test direct database connection using pymysql"""
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Test all tables
        tables = ['member', 'session', 'membership_type', 'membership', 'booking', 'payment']
        table_counts = {}
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cursor.fetchone()[0]
            except Exception as e:
                table_counts[table] = f"Error: {e}"
        
        print(f"Direct database connection successful!")
        print(f"Table counts:")
        for table, count in table_counts.items():
            print(f"  {table}: {count}")
        
        cursor.close()
        conn.close()
        return True, table_counts
        
    except Exception as e:
        print(f"Direct database connection failed: {e}")
        return False, {}

def init_db():
    """Initialize database connection - DON'T create new tables, use existing data"""
    print("Initializing database connection...")
    
    # Test direct connection first
    success, table_counts = test_database_connection()
    
    if success:
        print("Database connection successful!")
        print("Using existing database with data:")
        for table, count in table_counts.items():
            print(f"  {table}: {count} records")
        
        # Initialize SQLAlchemy but don't create tables
        try:
            # DON'T call db.create_all() - this would create empty tables
            print("SQLAlchemy initialized for authentication")
            print("Using existing database structure")
        except Exception as e:
            print(f"SQLAlchemy setup warning: {e}")
    else:
        print("Direct database connection failed!")
        print("Please check your database configuration")

# Member API endpoints using direct database queries
@app.route('/api/members')
def get_members():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MEMBER_ID, MEMBER_Title, MEMBER_Name, MEMBER_Gender, 
                   MEMBER_DOB, MEMBER_Phone, MEMBER_Email, MEMBER_EmgContactName, 
                   MEMBER_EmgContactPhone, MEMBER_Type,MEMBER_JCID,MEMBER_JCCompUsrnme
            FROM member
            ORDER BY MEMBER_ID
        """)
        
        members_data = []
        for row in cursor.fetchall():
            members_data.append({
                'member_id': row[0],
                'title': row[1],
                'name': row[2],
                'gender': row[3],
                'dob': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'phone': row[5],
                'email': row[6],
                'emergency_contact_name': row[7],
                'emergency_contact_phone': row[8],
                'type': row[9],
                'jcid': row[10],
                'jcusername': row[11],
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'members': members_data,
            'count': len(members_data)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'members': [],
            'count': 0
        }), 500

@app.route('/api/members/<int:member_id>')
def get_member(member_id):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MEMBER_ID, MEMBER_Title, MEMBER_Name, MEMBER_Gender, 
                   MEMBER_DOB, MEMBER_Phone, MEMBER_Email, MEMBER_EmgContactName, 
                   MEMBER_EmgContactPhone, MEMBER_Type
            FROM member
            WHERE MEMBER_ID = %s
        """, (member_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({
                'member_id': row[0],
                'title': row[1],
                'name': row[2],
                'gender': row[3],
                'dob': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'phone': row[5],
                'email': row[6],
                'emergency_contact_name': row[7],
                'emergency_contact_phone': row[8],
                'type': row[9]
            })
        else:
            return jsonify({'error': 'Member not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members/search')
def search_members():
    try:
        query = request.args.get('q', '')
        member_type = request.args.get('type', '')
        
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
            SELECT MEMBER_ID, MEMBER_Title, MEMBER_Name, MEMBER_Gender, 
                   MEMBER_DOB, MEMBER_Phone, MEMBER_Email, MEMBER_EmgContactName, 
                   MEMBER_EmgContactPhone, MEMBER_Type
            FROM member
            WHERE 1=1
        """
        params = []
        
        if query:
            sql += " AND (MEMBER_Name LIKE %s OR MEMBER_Email LIKE %s)"
            params.extend([f'%{query}%', f'%{query}%'])
        
        if member_type:
            sql += " AND MEMBER_Type = %s"
            params.append(member_type)
        
        sql += " ORDER BY MEMBER_ID"
        
        cursor.execute(sql, params)
        
        members_data = []
        for row in cursor.fetchall():
            members_data.append({
                'member_id': row[0],
                'title': row[1],
                'name': row[2],
                'gender': row[3],
                'dob': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'phone': row[5],
                'email': row[6],
                'emergency_contact_name': row[7],
                'emergency_contact_phone': row[8],
                'type': row[9]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'members': members_data,
            'count': len(members_data),
            'query': query,
            'type_filter': member_type
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Session endpoints
@app.route('/api/sessions')
def get_sessions():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SESSION_ID, SESSION_Date, SESSION_Time, SESSION_Capacity
            FROM session
            ORDER BY SESSION_Date, SESSION_Time
        """)
        
        sessions_data = []
        for row in cursor.fetchall():
            sessions_data.append({
                'session_id': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else None,
                'time': str(row[2]) if row[2] else None,
                'capacity': row[3]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'sessions': sessions_data,
            'count': len(sessions_data)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'sessions': [],
            'count': 0
        }), 500

@app.route('/api/sessions/<int:session_id>')
def get_session(session_id):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SESSION_ID, SESSION_Date, SESSION_Time, SESSION_Capacity
            FROM session
            WHERE SESSION_ID = %s
        """, (session_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({
                'session_id': row[0],
                'date': row[1].strftime('%Y-%m-%d') if row[1] else None,
                'time': str(row[2]) if row[2] else None,
                'capacity': row[3]
            })
        else:
            return jsonify({'error': 'Session not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Membership endpoints
@app.route('/api/memberships')
def get_memberships():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MEMBERSHIP_ID, MEMBER_ID, MEM_TYPE_ID, MEMBERSHIP_StartDate, 
                   MEMBERSHIP_ExpDate, MEMBERSHIP_Declared
            FROM membership
            ORDER BY MEMBERSHIP_ID
        """)
        
        memberships_data = []
        for row in cursor.fetchall():
            memberships_data.append({
                'membership_id': row[0],
                'member_id': row[1],
                'membership_type_id': row[2],
                'start_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'expiry_date': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'declared': bool(row[5])
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'memberships': memberships_data,
            'count': len(memberships_data)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'memberships': [],
            'count': 0
        }), 500

@app.route('/api/membership-types')
def get_membership_types():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MEM_TYPE_ID, MEM_TYPE_Name, MEM_TYPE_Fee
            FROM membership_type
            ORDER BY MEM_TYPE_ID
        """)
        
        types_data = []
        for row in cursor.fetchall():
            types_data.append({
                'type_id': row[0],
                'name': row[1],
                'fee': float(row[2])
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'membership_types': types_data,
            'count': len(types_data)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'membership_types': [],
            'count': 0
        }), 500

# Booking endpoints
@app.route('/api/bookings')
def get_bookings():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, 
                   BOOKING_Time, BOOKING_Status
            FROM booking
            ORDER BY BOOKING_Date DESC, BOOKING_Time DESC
        """)
        
        bookings_data = []
        for row in cursor.fetchall():
            bookings_data.append({
                'booking_ref': row[0],
                'member_id': row[1],
                'session_id': row[2],
                'booking_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'booking_time': str(row[4]) if row[4] else None,
                'status': row[5]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'bookings': bookings_data,
            'count': len(bookings_data)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'bookings': [],
            'count': 0
        }), 500

@app.route('/api/bookings/<booking_ref>')
def get_booking(booking_ref):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, 
                   BOOKING_Time, BOOKING_Status
            FROM booking
            WHERE BOOKING_Ref = %s
        """, (booking_ref,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({
                'booking_ref': row[0],
                'member_id': row[1],
                'session_id': row[2],
                'booking_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'booking_time': str(row[4]) if row[4] else None,
                'status': row[5]
            })
        else:
            return jsonify({'error': 'Booking not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payment endpoints
@app.route('/api/payments')
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
        
        payments_data = []
        for row in cursor.fetchall():
            payments_data.append({
                'payment_id': row[0],
                'membership_id': row[1],
                'payment_date': row[2].strftime('%Y-%m-%d') if row[2] else None,
                'total_fee': float(row[3]),
                'payment_type': row[4],
                'receipt_number': row[5],
                'verified_by': row[6]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'payments': payments_data,
            'count': len(payments_data)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'payments': [],
            'count': 0
        }), 500

@app.route('/api/payments/<int:payment_id>')
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

# Test database connection endpoint
@app.route('/api/test-db')
def test_db():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Test all tables
        tables = ['member', 'session', 'membership_type', 'membership', 'booking', 'payment']
        table_info = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_info[table] = count
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Database connection successful',
            'connection_config': {
                'host': db_config['host'],
                'port': db_config['port'],
                'database': db_config['database'],
                'user': db_config['user']
            },
            'table_counts': table_info
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}',
            'connection_config': {
                'host': db_config['host'],
                'port': db_config['port'],
                'database': db_config['database'],
                'user': db_config['user']
            }
        }), 500
@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        booking_date = data.get('booking_date')  # format: "YYYY-MM-DD"
        booking_time = data.get('booking_time')  # format: "HH:MM"
        status = data.get('status', 'Pending')

        if not session_id or not booking_date or not booking_time:
            return jsonify({'error': 'Missing required fields'}), 400

        booking_ref = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO booking (BOOKING_Ref, MEMBER_ID, SESSION_ID, BOOKING_Date, BOOKING_Time, BOOKING_Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            booking_ref,
            current_user.MEMBER_ID,
            session_id,
            booking_date,
            booking_time,
            status
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Booking created', 'booking_ref': booking_ref}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/bookings/<booking_ref>', methods=['PUT'])
@login_required
def update_booking(booking_ref):
    try:
        data = request.get_json()

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MEMBER_ID FROM booking WHERE BOOKING_Ref = %s
        """, (booking_ref,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Booking not found'}), 404
        if result[0] != current_user.MEMBER_ID:
            return jsonify({'error': 'Unauthorized'}), 403

        fields = []
        values = []

        if 'session_id' in data:
            fields.append("SESSION_ID = %s")
            values.append(data['session_id'])
        if 'booking_date' in data:
            fields.append("BOOKING_Date = %s")
            values.append(data['booking_date'])
        if 'booking_time' in data:
            fields.append("BOOKING_Time = %s")
            values.append(data['booking_time'])
        if 'status' in data:
            fields.append("BOOKING_Status = %s")
            values.append(data['status'])

        if not fields:
            return jsonify({'error': 'No fields to update'}), 400

        values.append(booking_ref)
        sql = f"UPDATE booking SET {', '.join(fields)} WHERE BOOKING_Ref = %s"

        cursor.execute(sql, tuple(values))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Booking updated'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/bookings/<booking_ref>', methods=['DELETE'])
@login_required
def delete_booking(booking_ref):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT MEMBER_ID FROM booking WHERE BOOKING_Ref = %s", (booking_ref,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Booking not found'}), 404
        if result[0] != current_user.MEMBER_ID:
            return jsonify({'error': 'Unauthorized'}), 403

        cursor.execute("DELETE FROM booking WHERE BOOKING_Ref = %s", (booking_ref,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Booking deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'path': request.path,
        'method': request.method
    }), 404

if __name__ == '__main__':
    print("Starting JCU Gym Management System...")
    print("Using existing database data (not creating new tables)")
    
    with app.app_context():
        # Initialize database connection but don't create new tables
        init_db()
    
    
    print("Auth blueprint registered successfully")
    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=5000, debug=True)  # 修复：使用 127.0.0.1 而不是 0.0.0.1