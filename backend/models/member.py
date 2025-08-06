from flask_login import UserMixin
from . import db

class Member(UserMixin, db.Model):
    __tablename__ = 'member'  # Correct double underscores

    MEMBER_ID = db.Column(db.Integer, primary_key=True)
    MEMBER_Title = db.Column(db.Enum('Mr', 'Mrs', 'Ms'), nullable=False)
    MEMBER_Name = db.Column(db.String(45), nullable=False)
    MEMBER_Gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    MEMBER_DOB = db.Column(db.Date, nullable=False)
    MEMBER_Phone = db.Column(db.String(20), nullable=False)
    MEMBER_Email = db.Column(db.String(100), nullable=False)
    MEMBER_EmgContactName = db.Column(db.String(45))
    MEMBER_EmgContactPhone = db.Column(db.String(20))
    MEMBER_PwdHash = db.Column(db.String(60), nullable=False)
    MEMBER_Type = db.Column(db.Enum('Student', 'Staff'), nullable=False)
    MEMBER_JCID = db.Column(db.BigInteger)
    MEMBER_JCCompUsrnme = db.Column(db.String(100))

    def get_id(self):
        """Required by Flask-Login"""
        return str(self.MEMBER_ID)

    def to_dict(self):
        """Convert member instance to dictionary format"""
        return {
            'id': self.MEMBER_ID,
            'title': self.MEMBER_Title,
            'name': self.MEMBER_Name,
            'gender': self.MEMBER_Gender,
            'dob': self.MEMBER_DOB.strftime('%Y-%m-%d') if self.MEMBER_DOB else None,
            'phone': self.MEMBER_Phone,
            'email': self.MEMBER_Email,
            'type': self.MEMBER_Type,
            'emergency_contact_name': self.MEMBER_EmgContactName,
            'emergency_contact_phone': self.MEMBER_EmgContactPhone,
            'jc_id': self.MEMBER_JCID,
            'jc_username': self.MEMBER_JCCompUsrnme
        }

    def __repr__(self):
        return f'<Member {self.MEMBER_Name}>'
