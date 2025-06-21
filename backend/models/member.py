from . import db

class Member(db.Model):
    __tablename__ = 'member'
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
