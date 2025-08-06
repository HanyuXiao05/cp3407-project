from app import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'booking'
    
    BOOKING_Ref = db.Column(db.String(12), primary_key=True)
    MEMBER_ID = db.Column(db.Integer, db.ForeignKey('member.MEMBER_ID'), nullable=False)
    SESSION_ID = db.Column(db.Integer, db.ForeignKey('session.SESSION_ID'), nullable=False)
    BOOKING_Date = db.Column(db.Date, nullable=False)
    BOOKING_Time = db.Column(db.Time, nullable=False)
    BOOKING_Status = db.Column(db.Enum('Booked', 'Deleted', 'Attended', 'No-Show'), nullable=False)
    
    # 关联
    session = db.relationship('Session', backref='bookings', lazy=True)
    
    def __init__(self, member_id, session_id):
        from uuid import uuid4
        self.BOOKING_Ref = str(uuid4())[:12]
        self.MEMBER_ID = member_id
        self.SESSION_ID = session_id
        self.BOOKING_Date = datetime.now().date()
        self.BOOKING_Time = datetime.now().time()
        self.BOOKING_Status = 'Booked'
    
    def to_dict(self):
        return {
            'booking_ref': self.BOOKING_Ref,
            'member_id': self.MEMBER_ID,
            'session_id': self.SESSION_ID,
            'booking_date': self.BOOKING_Date.strftime('%Y-%m-%d'),
            'booking_time': self.BOOKING_Time.strftime('%H:%M:%S'),
            'status': self.BOOKING_Status
        } 