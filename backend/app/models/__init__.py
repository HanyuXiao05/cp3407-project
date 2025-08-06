from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base model class that all other models will inherit from"""
    __abstract__ = True
    
    def save(self):
        """Save the model instance to the database"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the model instance from the database"""
        db.session.delete(self)
        db.session.commit()
        return self

# Import all models here to avoid circular imports
from app.models.member import Member
from app.models.session import Session
from app.models.booking import Booking
from app.models.membership import Membership
from app.models.membership_type import MembershipType
from app.models.payment import Payment

__all__ = [
    'Member',
    'Session',
    'Booking',
    'Membership',
    'MembershipType',
    'Payment'
]
