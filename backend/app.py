from flask import Flask, jsonify
from models import db
from models.member import Member
from models.booking import Booking
from models.session import Session
from models.membership import Membership
from models.membership_type import MembershipType
from models.payment import Payment
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return "JCU Gym Management System API"

@app.route('/api/members')
def get_members():
    members = Member.query.all()
    return jsonify([
        {
            "MEMBER_ID": m.MEMBER_ID,
            "MEMBER_Name": m.MEMBER_Name,
            "MEMBER_Email": m.MEMBER_Email
        } for m in members
    ])

@app.route('/api/bookings')
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([
        {
            "BOOKING_Ref": b.BOOKING_Ref,
            "MEMBER_ID": b.MEMBER_ID,
            "SESSION_ID": b.SESSION_ID,
            "BOOKING_Date": str(b.BOOKING_Date),
            "BOOKING_Time": str(b.BOOKING_Time),
            "BOOKING_Status": b.BOOKING_Status
        } for b in bookings
    ])

@app.route('/api/sessions')
def get_sessions():
    sessions = Session.query.all()
    return jsonify([
        {
            "SESSION_ID": s.SESSION_ID,
            "SESSION_Date": str(s.SESSION_Date),
            "SESSION_Time": str(s.SESSION_Time),
            "SESSION_Capacity": s.SESSION_Capacity
        } for s in sessions
    ])

@app.route('/api/memberships')
def get_memberships():
    memberships = Membership.query.all()
    return jsonify([
        {
            "MEMBERSHIP_ID": m.MEMBERSHIP_ID,
            "MEMBER_ID": m.MEMBER_ID,
            "MEM_TYPE_ID": m.MEM_TYPE_ID,
            "MEMBERSHIP_StartDate": str(m.MEMBERSHIP_StartDate),
            "MEMBERSHIP_ExpDate": str(m.MEMBERSHIP_ExpDate),
            "MEMBERSHIP_Declared": m.MEMBERSHIP_Declared
        } for m in memberships
    ])

@app.route('/api/membership_types')
def get_membership_types():
    types = MembershipType.query.all()
    return jsonify([
        {
            "MEM_TYPE_ID": t.MEM_TYPE_ID,
            "MEM_TYPE_Name": t.MEM_TYPE_Name,
            "MEM_TYPE_Fee": float(t.MEM_TYPE_Fee)
        } for t in types
    ])

@app.route('/api/payments')
def get_payments():
    payments = Payment.query.all()
    return jsonify([
        {
            "PAYMENT_ID": p.PAYMENT_ID,
            "MEMBERSHIP_ID": p.MEMBERSHIP_ID,
            "PAYMENT_Date": str(p.PAYMENT_Date),
            "PAYMENT_TotalFee": float(p.PAYMENT_TotalFee),
            "PAYMENT_Type": p.PAYMENT_Type,
            "PAYMENT_RcptNum": p.PAYMENT_RcptNum,
            "PAYMENT_RcptVerifiedBy": p.PAYMENT_RcptVerifiedBy
        } for p in payments
    ])

if __name__ == '__main__':
    app.run(debug=True)
