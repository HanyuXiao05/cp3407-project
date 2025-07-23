from app import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'session'
    
    SESSION_ID = db.Column(db.Integer, primary_key=True)
    SESSION_Date = db.Column(db.Date, nullable=False)
    SESSION_Time = db.Column(db.Time, nullable=False)
    SESSION_Capacity = db.Column(db.Integer, nullable=False)
    
    def __init__(self, date, time, capacity):
        self.SESSION_Date = date
        self.SESSION_Time = time
        self.SESSION_Capacity = capacity
    
    @property
    def available_slots(self):
        booked_count = len([b for b in self.bookings if b.BOOKING_Status == 'Booked'])
        return self.SESSION_Capacity - booked_count
    
    @property
    def is_full(self):
        return self.available_slots <= 0
    
    @property
    def is_past(self):
        session_datetime = datetime.combine(self.SESSION_Date, self.SESSION_Time)
        return session_datetime < datetime.now()
    
    def to_dict(self):
        return {
            'session_id': self.SESSION_ID,
            'date': self.SESSION_Date.strftime('%Y-%m-%d'),
            'time': self.SESSION_Time.strftime('%H:%M:%S'),
            'capacity': self.SESSION_Capacity,
            'available_slots': self.available_slots,
            'is_full': self.is_full,
            'is_past': self.is_past
        } 