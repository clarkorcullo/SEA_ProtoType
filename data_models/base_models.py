"""
Base models and mixins for the Social Engineering Awareness Program
Provides common functionality and inheritance structure
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from typing import Optional, Dict, Any

db = SQLAlchemy()

class TimestampMixin:
    """Mixin to add timestamp fields to models"""
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary with timestamps"""
        return {
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BaseModel(db.Model):
    """Abstract base model with common functionality"""
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    
    @declared_attr
    def __tablename__(cls):
        """Generate table name from class name"""
        return cls.__name__.lower()
    
    def save(self) -> bool:
        """Save the model to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving {self.__class__.__name__}: {e}")
            return False
    
    def delete(self) -> bool:
        """Delete the model from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting {self.__class__.__name__}: {e}")
            return False
    
    def update(self, **kwargs) -> bool:
        """Update model attributes"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating {self.__class__.__name__}: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    @classmethod
    def get_by_id(cls, id: int):
        """Get model by ID"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all instances of the model"""
        return cls.query.all()
    
    @classmethod
    def count(cls) -> int:
        """Get total count of model instances"""
        return cls.query.count()
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

