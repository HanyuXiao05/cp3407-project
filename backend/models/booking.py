from . import db

class Booking(db.Model):
    __tablename__ = 'booking'
    BOOKING_Ref = db.Column(db.String(12), primary_key=True)
    MEMBER_ID = db.Column(db.Integer, db.ForeignKey('member.MEMBER_ID'), nullable=False)
    SESSION_ID = db.Column(db.Integer, db.ForeignKey('session.SESSION_ID'), nullable=False)
    BOOKING_Date = db.Column(db.Date, nullable=False)
    BOOKING_Time = db.Column(db.Time, nullable=False)
    BOOKING_Status = db.Column(db.Enum('Booked', 'Deleted', 'Attended', 'No-Show'), nullable=False)
