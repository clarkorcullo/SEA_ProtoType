"""
User-related models for the Social Engineering Awareness Program
Includes User and PasswordResetToken models with enhanced functionality
"""

from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, List, Dict, Any
import secrets
import re

from .base_models import BaseModel, TimestampMixin, db

class User(UserMixin, BaseModel, TimestampMixin):
    """User model with authentication and progress tracking"""
    
    # Basic user information
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    year_level = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(200), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    
    # Progress tracking attributes
    modules_completed = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    simulations_completed = db.Column(db.Integer, default=0)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    assessment_results = db.relationship('AssessmentResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    simulation_results = db.relationship('SimulationResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    feedback_surveys = db.relationship('FeedbackSurvey', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    password_reset_tokens = db.relationship('PasswordResetToken', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        """Initialize user with password hashing"""
        if 'password' in kwargs:
            kwargs['password_hash'] = generate_password_hash(kwargs.pop('password'))
        super().__init__(**kwargs)
    
    @property
    def age(self) -> Optional[int]:
        """Calculate user age from birthday"""
        if self.birthday:
            today = datetime.now()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return None
    
    @property
    def completion_percentage(self) -> float:
        """Calculate overall completion percentage"""
        total_modules = 5  # Total number of modules in the program
        if total_modules == 0:
            return 0.0
        return (self.modules_completed / total_modules) * 100
    
    @property
    def average_score(self) -> float:
        """Calculate average score across all assessments"""
        total_assessments = self.assessment_results.count()
        if total_assessments == 0:
            return 0.0
        return self.total_score / total_assessments
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an administrator"""
        return self.username == 'administrator'
    
    def set_password(self, password: str) -> bool:
        """Set user password with validation"""
        if self._validate_password(password):
            self.password_hash = generate_password_hash(password)
            return True
        return False
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches"""
        return check_password_hash(self.password_hash, password)
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 12:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    def update_progress(self, module_id: int, score: int, status: str = 'completed') -> bool:
        """Update user progress for a specific module"""
        try:
            progress = UserProgress.query.filter_by(user_id=self.id, module_id=module_id).first()
            if not progress:
                progress = UserProgress(user_id=self.id, module_id=module_id)
            
            progress.score = score
            progress.status = status
            progress.completed_at = datetime.utcnow()
            progress.save()
            
            # Update overall progress
            self.modules_completed = UserProgress.query.filter_by(
                user_id=self.id, status='completed'
            ).count()
            self.total_score += score
            self.save()
            
            return True
        except Exception as e:
            print(f"Error updating progress: {e}")
            return False
    
    def sync_progress_counters(self) -> bool:
        """Sync user progress counters with actual data"""
        try:
            from data_models.progress_models import UserProgress, SimulationResult
            
            # Count completed modules
            completed_progress = UserProgress.query.filter_by(
                user_id=self.id, status='completed'
            ).all()
            self.modules_completed = len(completed_progress)
            
            # Calculate total score from highest scores achieved
            total_score = 0
            for progress in completed_progress:
                # Use highest score for completed modules
                total_score += max(progress.score, progress.highest_score)
            self.total_score = total_score
            
            # Count completed simulations
            completed_simulations = SimulationResult.query.filter_by(
                user_id=self.id, completed=True
            ).count()
            self.simulations_completed = completed_simulations
            
            return self.save()
            
        except Exception as e:
            print(f"Error syncing progress counters: {e}")
            return False
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get comprehensive progress summary"""
        return {
            'user_id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'modules_completed': self.modules_completed,
            'total_score': self.total_score,
            'simulations_completed': self.simulations_completed,
            'completion_percentage': self.completion_percentage,
            'average_score': self.average_score,
            'total_assessments': self.assessment_results.count(),
            'total_simulations': self.simulation_results.count()
        }
    
    def create_password_reset_token(self) -> Optional[str]:
        """Create a password reset token"""
        try:
            # Invalidate existing tokens
            PasswordResetToken.query.filter_by(user_id=self.id, used=False).update({'used': True})
            
            # Create new token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)
            
            reset_token = PasswordResetToken(
                user_id=self.id,
                token=token,
                expires_at=expires_at
            )
            reset_token.save()
            
            return token
        except Exception as e:
            print(f"Error creating reset token: {e}")
            return None
    
    @classmethod
    def get_by_username(cls, username: str):
        """Get user by username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email: str):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_top_performers(cls, limit: int = 10) -> List['User']:
        """Get top performing users by total score"""
        return cls.query.order_by(cls.total_score.desc()).limit(limit).all()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary with additional properties"""
        base_dict = super().to_dict()
        base_dict.update({
            'age': self.age,
            'completion_percentage': self.completion_percentage,
            'average_score': self.average_score
        })
        return base_dict

class PasswordResetToken(BaseModel, TimestampMixin):
    """Password reset token model"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    
    def is_valid(self) -> bool:
        """Check if token is valid and not expired"""
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self) -> bool:
        """Mark token as used"""
        return self.update(used=True)
    
    @classmethod
    def get_valid_token(cls, token: str):
        """Get valid token by string"""
        token_obj = cls.query.filter_by(token=token).first()
        if token_obj and token_obj.is_valid():
            return token_obj
        return None
    
    @classmethod
    def cleanup_expired_tokens(cls) -> int:
        """Clean up expired tokens and return count of deleted tokens"""
        try:
            expired_tokens = cls.query.filter(
                cls.expires_at < datetime.utcnow()
            ).all()
            
            count = len(expired_tokens)
            for token in expired_tokens:
                token.delete()
            
            return count
        except Exception as e:
            print(f"Error cleaning up expired tokens: {e}")
            return 0

