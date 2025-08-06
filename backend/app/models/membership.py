from app import db
from datetime import datetime, timedelta

class Membership(db.Model):
    __tablename__ = 'membership'
    
    MEMBERSHIP_ID = db.Column(db.Integer, primary_key=True)
    MEMBER_ID = db.Column(db.Integer, db.ForeignKey('member.MEMBER_ID'), nullable=False)
    MEM_TYPE_ID = db.Column(db.Integer, db.ForeignKey('membership_type.MEM_TYPE_ID'), nullable=False)
    MEMBERSHIP_StartDate = db.Column(db.Date, nullable=False)
    MEMBERSHIP_ExpDate = db.Column(db.Date, nullable=False)
    MEMBERSHIP_Declared = db.Column(db.Boolean, nullable=False, default=False)
    
    # 关联
    payments = db.relationship('Payment', backref='membership', lazy=True)
    
    @property
    def is_active(self):
        return self.MEMBERSHIP_ExpDate >= datetime.now().date()
    
    @property
    def days_remaining(self):
        if not self.is_active:
            return 0
        return (self.MEMBERSHIP_ExpDate - datetime.now().date()).days
    
    def to_dict(self):
        return {
            'membership_id': self.MEMBERSHIP_ID,
            'member_id': self.MEMBER_ID,
            'type_id': self.MEM_TYPE_ID,
            'start_date': self.MEMBERSHIP_StartDate.strftime('%Y-%m-%d'),
            'expiry_date': self.MEMBERSHIP_ExpDate.strftime('%Y-%m-%d'),
            'is_declared': self.MEMBERSHIP_Declared,
            'is_active': self.is_active,
            'days_remaining': self.days_remaining
        } 