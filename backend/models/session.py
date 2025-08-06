from . import db

class Session(db.Model):
    __tablename__ = 'session'
    SESSION_ID = db.Column(db.Integer, primary_key=True)
    SESSION_Date = db.Column(db.Date, nullable=False)
    SESSION_Time = db.Column(db.Time, nullable=False)
    SESSION_Capacity = db.Column(db.Integer, nullable=False)
