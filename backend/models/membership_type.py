from . import db

class MembershipType(db.Model):
    __tablename__ = 'membership_type'
    MEM_TYPE_ID = db.Column(db.Integer, primary_key=True)
    MEM_TYPE_Name = db.Column(db.String(45), nullable=False)
    MEM_TYPE_Fee = db.Column(db.Numeric(6, 2), nullable=False)
