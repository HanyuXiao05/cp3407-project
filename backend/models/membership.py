from . import db


class Membership(db.Model):
    __tablename__ = 'membership'
    MEMBERSHIP_ID = db.Column(db.Integer, primary_key=True)
    MEMBER_ID = db.Column(db.Integer, db.ForeignKey('member.MEMBER_ID'), nullable=False)
    MEM_TYPE_ID = db.Column(db.Integer, db.ForeignKey('membership_type.MEM_TYPE_ID'), nullable=False)
    MEMBERSHIP_StartDate = db.Column(db.Date, nullable=False)
    MEMBERSHIP_ExpDate = db.Column(db.Date, nullable=False)
    MEMBERSHIP_Declared = db.Column(db.Boolean, nullable=False)
