from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payment'
    
    PAYMENT_ID = db.Column(db.Integer, primary_key=True)
    MEMBERSHIP_ID = db.Column(db.Integer, db.ForeignKey('membership.MEMBERSHIP_ID'), nullable=False)
    PAYMENT_Date = db.Column(db.Date, nullable=False)
    PAYMENT_TotalFee = db.Column(db.Numeric(6, 2), nullable=False)
    PAYMENT_Type = db.Column(db.Enum('Cash', 'Cheque', 'NETS', 'MasterCard', 'Visa', 'Amex', 'Union Pay', 'Salary Deduction'), nullable=False)
    PAYMENT_RcptNum = db.Column(db.String(20))
    PAYMENT_RcptVerifiedBy = db.Column(db.String(20))
    
    def __init__(self, membership_id, total_fee, payment_type):
        self.MEMBERSHIP_ID = membership_id
        self.PAYMENT_Date = datetime.now().date()
        self.PAYMENT_TotalFee = total_fee
        self.PAYMENT_Type = payment_type
    
    def to_dict(self):
        return {
            'payment_id': self.PAYMENT_ID,
            'membership_id': self.MEMBERSHIP_ID,
            'date': self.PAYMENT_Date.strftime('%Y-%m-%d'),
            'total_fee': float(self.PAYMENT_TotalFee),
            'payment_type': self.PAYMENT_Type,
            'receipt_number': self.PAYMENT_RcptNum,
            'verified_by': self.PAYMENT_RcptVerifiedBy
        } 