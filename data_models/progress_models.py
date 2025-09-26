"""
Progress tracking models for the Social Engineering Awareness Program
Includes UserProgress, AssessmentResult, SimulationResult, and FeedbackSurvey models
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import json

from .base_models import BaseModel, TimestampMixin, db

class ProgressStatus(Enum):
    """Enum for progress status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class AssessmentType(Enum):
    """Enum for assessment types"""
    BASELINE = "baseline"
    KNOWLEDGE_CHECK = "knowledge_check"
    FINAL_ASSESSMENT = "final_assessment"
    FOLLOW_UP = "follow_up"

class SimulationType(Enum):
    """Enum for simulation types"""
    PHISHING = "phishing"
    PRETEXTING = "pretexting"
    BAITING = "baiting"
    QUID_PRO_QUO = "quid_pro_quo"

class UserProgress(BaseModel, TimestampMixin):
    """User progress tracking model"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    status = db.Column(db.String(20), default=ProgressStatus.NOT_STARTED.value)
    score = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # in minutes
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, **kwargs):
        """Initialize progress with validation"""
        if 'status' in kwargs:
            if kwargs['status'] not in [e.value for e in ProgressStatus]:
                raise ValueError(f"Invalid status: {kwargs['status']}")
        super().__init__(**kwargs)
    
    @property
    def is_completed(self) -> bool:
        """Check if progress is completed"""
        return self.status == ProgressStatus.COMPLETED.value
    
    @property
    def completion_time(self) -> Optional[int]:
        """Get completion time in minutes"""
        if self.completed_at and self.created_at:
            delta = self.completed_at - self.created_at
            return int(delta.total_seconds() / 60)
        return None
    
    def start_progress(self) -> bool:
        """Start progress tracking"""
        return self.update(
            status=ProgressStatus.IN_PROGRESS.value,
            attempts=self.attempts + 1
        )
    
    def complete_progress(self, score: int) -> bool:
        """Complete progress with score"""
        return self.update(
            status=ProgressStatus.COMPLETED.value,
            score=score,
            completed_at=datetime.utcnow()
        )
    
    def update_time_spent(self, minutes: int) -> bool:
        """Update time spent on module"""
        return self.update(time_spent=self.time_spent + minutes)
    
    @classmethod
    def get_user_progress(cls, user_id: int) -> List['UserProgress']:
        """Get all progress for a user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at).all()
    
    @classmethod
    def get_module_progress(cls, user_id: int, module_id: int):
        """Get progress for specific module and user"""
        return cls.query.filter_by(user_id=user_id, module_id=module_id).first()
    
    @classmethod
    def get_completed_modules(cls, user_id: int) -> List['UserProgress']:
        """Get completed modules for a user"""
        return cls.query.filter_by(
            user_id=user_id, 
            status=ProgressStatus.COMPLETED.value
        ).all()

class AssessmentResult(BaseModel, TimestampMixin):
    """Assessment result tracking model"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, default=0)  # in seconds
    passed = db.Column(db.Boolean, default=False)
    answers_data = db.Column(db.Text, nullable=True)  # JSON string of answers
    
    def __init__(self, **kwargs):
        """Initialize assessment result with validation"""
        if 'assessment_type' in kwargs:
            if kwargs['assessment_type'] not in [e.value for e in AssessmentType]:
                raise ValueError(f"Invalid assessment type: {kwargs['assessment_type']}")
        super().__init__(**kwargs)
    
    @property
    def percentage_score(self) -> float:
        """Calculate percentage score"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100
    
    @property
    def time_taken_minutes(self) -> float:
        """Get time taken in minutes"""
        return self.time_taken / 60
    
    def set_answers_data(self, answers: Dict[str, Any]) -> bool:
        """Set answers data as JSON"""
        try:
            self.answers_data = json.dumps(answers)
            return True
        except Exception as e:
            print(f"Error setting answers data: {e}")
            return False
    
    def get_answers_data(self) -> Optional[Dict[str, Any]]:
        """Get answers data from JSON"""
        if not self.answers_data:
            return None
        try:
            return json.loads(self.answers_data)
        except Exception as e:
            print(f"Error parsing answers data: {e}")
            return None
    
    def calculate_pass_status(self, passing_threshold: float = 70.0) -> bool:
        """Calculate if assessment was passed"""
        self.passed = self.percentage_score >= passing_threshold
        return self.passed
    
    @classmethod
    def get_user_assessments(cls, user_id: int, assessment_type: Optional[str] = None) -> List['AssessmentResult']:
        """Get assessments for a user"""
        query = cls.query.filter_by(user_id=user_id)
        if assessment_type:
            query = query.filter_by(assessment_type=assessment_type)
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_best_score(cls, user_id: int, assessment_type: str) -> Optional['AssessmentResult']:
        """Get best score for a specific assessment type"""
        return cls.query.filter_by(
            user_id=user_id, 
            assessment_type=assessment_type
        ).order_by(cls.score.desc()).first()
    
    @classmethod
    def get_average_score(cls, assessment_type: str) -> float:
        """Get average score for an assessment type"""
        result = db.session.query(db.func.avg(cls.score)).filter_by(
            assessment_type=assessment_type
        ).scalar()
        return float(result) if result else 0.0

class SimulationResult(BaseModel, TimestampMixin):
    """Simulation result tracking model"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)  # Link to specific module
    simulation_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    decisions_made = db.Column(db.Text, nullable=True)  # JSON string of decisions
    time_taken = db.Column(db.Integer, default=0)  # in seconds
    completed = db.Column(db.Boolean, default=False)
    scenario_data = db.Column(db.Text, nullable=True)  # JSON string of scenario details
    
    def __init__(self, **kwargs):
        """Initialize simulation result with validation"""
        if 'simulation_type' in kwargs:
            if kwargs['simulation_type'] not in [e.value for e in SimulationType]:
                raise ValueError(f"Invalid simulation type: {kwargs['simulation_type']}")
        super().__init__(**kwargs)
    
    @property
    def time_taken_minutes(self) -> float:
        """Get time taken in minutes"""
        return self.time_taken / 60
    
    def set_decisions_data(self, decisions: List[Dict[str, Any]]) -> bool:
        """Set decisions data as JSON"""
        try:
            self.decisions_made = json.dumps(decisions)
            return True
        except Exception as e:
            print(f"Error setting decisions data: {e}")
            return False
    
    def get_decisions_data(self) -> Optional[List[Dict[str, Any]]]:
        """Get decisions data from JSON"""
        if not self.decisions_made:
            return None
        try:
            return json.loads(self.decisions_made)
        except Exception as e:
            print(f"Error parsing decisions data: {e}")
            return None
    
    def set_scenario_data(self, scenario: Dict[str, Any]) -> bool:
        """Set scenario data as JSON"""
        try:
            self.scenario_data = json.dumps(scenario)
            return True
        except Exception as e:
            print(f"Error setting scenario data: {e}")
            return False
    
    def get_scenario_data(self) -> Optional[Dict[str, Any]]:
        """Get scenario data from JSON"""
        if not self.scenario_data:
            return None
        try:
            return json.loads(self.scenario_data)
        except Exception as e:
            print(f"Error parsing scenario data: {e}")
            return None
    
    def complete_simulation(self, score: int) -> bool:
        """Complete simulation with score"""
        return self.update(
            score=score,
            completed=True,
            time_taken=self.time_taken
        )
    
    @classmethod
    def get_user_simulations(cls, user_id: int, simulation_type: Optional[str] = None) -> List['SimulationResult']:
        """Get simulations for a user"""
        query = cls.query.filter_by(user_id=user_id)
        if simulation_type:
            query = query.filter_by(simulation_type=simulation_type)
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_completed_simulations(cls, user_id: int) -> List['SimulationResult']:
        """Get completed simulations for a user"""
        return cls.query.filter_by(
            user_id=user_id, 
            completed=True
        ).order_by(cls.created_at.desc()).all()

class FeedbackSurvey(BaseModel, TimestampMixin):
    """Feedback survey model"""
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 scale
    feedback_text = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.String(20), nullable=True)  # easy, medium, hard
    additional_questions = db.Column(db.Text, nullable=True)  # JSON string of additional questions
    
    def __init__(self, **kwargs):
        """Initialize feedback with validation"""
        if 'rating' in kwargs:
            rating = kwargs['rating']
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
        super().__init__(**kwargs)
    
    def set_additional_questions(self, questions: Dict[str, Any]) -> bool:
        """Set additional questions as JSON"""
        try:
            self.additional_questions = json.dumps(questions)
            return True
        except Exception as e:
            print(f"Error setting additional questions: {e}")
            return False
    
    def get_additional_questions(self) -> Optional[Dict[str, Any]]:
        """Get additional questions from JSON"""
        if not self.additional_questions:
            return None
        try:
            return json.loads(self.additional_questions)
        except Exception as e:
            print(f"Error parsing additional questions: {e}")
            return None
    
    @classmethod
    def get_module_feedback(cls, module_id: int) -> List['FeedbackSurvey']:
        """Get feedback for a specific module"""
        return cls.query.filter_by(module_id=module_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_average_rating(cls, module_id: Optional[int] = None) -> float:
        """Get average rating"""
        query = cls.query
        if module_id:
            query = query.filter_by(module_id=module_id)
        
        result = db.session.query(db.func.avg(cls.rating)).scalar()
        return float(result) if result else 0.0
    
    @classmethod
    def get_rating_distribution(cls, module_id: Optional[int] = None) -> Dict[int, int]:
        """Get rating distribution"""
        query = cls.query
        if module_id:
            query = query.filter_by(module_id=module_id)
        
        distribution = {}
        for rating in range(1, 6):
            count = query.filter_by(rating=rating).count()
            distribution[rating] = count
        
        return distribution

