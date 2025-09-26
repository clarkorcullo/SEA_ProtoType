#!/usr/bin/env python3
"""
Assessment-specific models for tracking attempts and results
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from data_models.base_models import BaseModel, TimestampMixin
from data_models.user_models import User
from data_models.content_models import FinalAssessmentQuestion
from data_models.base_models import db
import json

class AssessmentAttempt(BaseModel, TimestampMixin):
    """Track user attempts at the final assessment"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False, default=1)
    questions_used = db.Column(db.Text, nullable=False, default='[]')  # JSON string of question IDs
    answers = db.Column(db.Text, nullable=True)  # JSON string of user answers
    score = db.Column(db.Float, nullable=True)  # Percentage score
    passed = db.Column(db.Boolean, nullable=False, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    time_taken = db.Column(db.Integer, nullable=True)  # Time in seconds
    
    # Relationships
    user = db.relationship('User', backref='assessment_attempts')
    
    def __init__(self, **kwargs):
        """Initialize assessment attempt"""
        super().__init__(**kwargs)
    
    def set_questions_used(self, question_ids: List[int]) -> bool:
        """Set the questions used in this attempt"""
        try:
            self.questions_used = json.dumps(question_ids)
            return True
        except Exception as e:
            print(f"Error setting questions: {e}")
            return False
    
    def get_questions_used(self) -> List[int]:
        """Get the question IDs used in this attempt"""
        if not self.questions_used:
            return []
        try:
            return json.loads(self.questions_used)
        except Exception as e:
            print(f"Error parsing questions: {e}")
            return []
    
    def set_answers(self, answers: Dict[int, str]) -> bool:
        """Set user answers for this attempt"""
        try:
            self.answers = json.dumps(answers)
            return True
        except Exception as e:
            print(f"Error setting answers: {e}")
            return False
    
    def get_answers(self) -> Dict[int, str]:
        """Get user answers for this attempt"""
        if not self.answers:
            return {}
        try:
            return json.loads(self.answers)
        except Exception as e:
            print(f"Error parsing answers: {e}")
            return {}
    
    def calculate_score(self) -> float:
        """Calculate score based on correct answers"""
        if not self.answers:
            return 0.0
        
        question_ids = self.get_questions_used()
        user_answers = self.get_answers()
        
        if not question_ids:
            return 0.0
        
        correct_count = 0
        total_questions = len(question_ids)
        
        for question_id in question_ids:
            if question_id in user_answers:
                question = FinalAssessmentQuestion.get_by_id(question_id)
                if question and question.check_answer(user_answers[question_id]):
                    correct_count += 1
        
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0.0
        self.score = score
        self.passed = score >= 80.0  # 80% passing rate
        return score
    
    def is_eligible_for_retake(self) -> bool:
        """Check if user is eligible for another attempt"""
        # Check if 24 hours have passed since last attempt
        if not self.completed_at:
            return True
        
        time_since_completion = datetime.utcnow() - self.completed_at
        return time_since_completion >= timedelta(hours=24)
    
    @classmethod
    def get_user_attempts(cls, user_id: int) -> List['AssessmentAttempt']:
        """Get all attempts for a user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.attempt_number.desc()).all()
    
    @classmethod
    def get_latest_attempt(cls, user_id: int) -> Optional['AssessmentAttempt']:
        """Get the latest attempt for a user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.attempt_number.desc()).first()
    
    @classmethod
    def can_start_new_attempt(cls, user_id: int) -> bool:
        """Check if user can start a new attempt"""
        # Import here to avoid circular imports
        from data_models.user_models import User
        
        # Check if user is admin (exempt from limits)
        user = User.query.get(user_id)
        if user and user.is_admin:
            return True
        
        attempts = cls.get_user_attempts(user_id)
        
        # Check attempt limit (3 attempts)
        if len(attempts) >= 3:
            return False
        
        # Check 24-hour cooldown
        if attempts:
            latest_attempt = attempts[0]
            if not latest_attempt.is_eligible_for_retake():
                return False
        
        return True
    
    @classmethod
    def get_next_attempt_number(cls, user_id: int) -> int:
        """Get the next attempt number for a user"""
        attempts = cls.get_user_attempts(user_id)
        return len(attempts) + 1

class AssessmentSession(BaseModel, TimestampMixin):
    """Track active assessment sessions"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempt_id = db.Column(db.Integer, db.ForeignKey('assessmentattempt.id'), nullable=False)
    session_token = db.Column(db.String(100), nullable=False, unique=True, default='')
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', backref='assessment_sessions')
    attempt = db.relationship('AssessmentAttempt', backref='sessions')
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    def extend_session(self, hours: int = 2) -> bool:
        """Extend session expiration"""
        try:
            self.expires_at = datetime.utcnow() + timedelta(hours=hours)
            return True
        except Exception as e:
            print(f"Error extending session: {e}")
            return False
    
    @classmethod
    def create_session(cls, user_id: int, attempt_id: int, hours: int = 2) -> 'AssessmentSession':
        """Create a new assessment session"""
        import secrets
        import hashlib
        
        # Generate secure session token
        token_data = f"{user_id}_{attempt_id}_{datetime.utcnow().timestamp()}"
        session_token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
        
        session = cls(
            user_id=user_id,
            attempt_id=attempt_id,
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(hours=hours)
        )
        
        if session.save():
            return session
        return None
    
    @classmethod
    def get_active_session(cls, session_token: str) -> Optional['AssessmentSession']:
        """Get active session by token"""
        session = cls.query.filter_by(session_token=session_token, is_active=True).first()
        if session and not session.is_expired():
            return session
        return None
    
    @classmethod
    def invalidate_session(cls, session_token: str) -> bool:
        """Invalidate a session"""
        session = cls.query.filter_by(session_token=session_token).first()
        if session:
            session.is_active = False
            return session.save()
        return False
