from . import db

class Payment(db.Model):
    __tablename__ = 'payment'
    PAYMENT_ID = db.Column(db.Integer, primary_key=True)
    MEMBERSHIP_ID = db.Column(db.Integer, db.ForeignKey('membership.MEMBERSHIP_ID'), nullable=False)
    PAYMENT_Date = db.Column(db.Date, nullable=False)
    PAYMENT_TotalFee = db.Column(db.Numeric(6, 2), nullable=False)
    PAYMENT_Type = db.Column(db.Enum('Cash', 'Cheque', 'NETS', 'MasterCard', 'Visa', 'Amex', 'Union Pay', 'Salary Deduction'), nullable=False)
    PAYMENT_RcptNum = db.Column(db.String(20))
    PAYMENT_RcptVerifiedBy = db.Column(db.String(20))
    PAYMENT_IsSimulated = db.Column(db.Boolean, default=False)  # ✅ 新增字段
