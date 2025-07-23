# app/models/member.py
from app import db
from flask_login import UserMixin

class Member(db.Model, UserMixin):
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