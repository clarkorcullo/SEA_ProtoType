"""
Content models for the Social Engineering Awareness Program
Includes Module, KnowledgeCheckQuestion, and FinalAssessmentQuestion models
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from .base_models import BaseModel, TimestampMixin, db
from .progress_models import UserProgress

class ModuleStatus(Enum):
    """Enum for module status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class SimulationType(Enum):
    """Enum for simulation types"""
    PHISHING = "phishing"
    PRETEXTING = "pretexting"
    BAITING = "baiting"
    QUID_PRO_QUO = "quid_pro_quo"

class Module(BaseModel, TimestampMixin):
    """Module model for learning content"""
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False, unique=True)
    has_simulation = db.Column(db.Boolean, default=False)
    simulation_type = db.Column(db.String(50), nullable=True)
    
    # Relationships
    knowledge_questions = db.relationship('KnowledgeCheckQuestion', backref='module', lazy='dynamic', cascade='all, delete-orphan')
    user_progress = db.relationship('UserProgress', backref='module', lazy='dynamic', cascade='all, delete-orphan')
    feedback_surveys = db.relationship('FeedbackSurvey', backref='module', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        """Initialize module with validation"""
        if 'simulation_type' in kwargs and kwargs['simulation_type']:
            if kwargs['simulation_type'] not in [e.value for e in SimulationType]:
                raise ValueError(f"Invalid simulation type: {kwargs['simulation_type']}")
        super().__init__(**kwargs)
    
    @property
    def question_count(self) -> int:
        """Get number of knowledge check questions"""
        return self.knowledge_questions.count()
    
    @property
    def completion_rate(self) -> float:
        """Calculate completion rate for this module"""
        total_users = db.session.query(db.func.count(db.distinct(UserProgress.user_id))).scalar()
        if total_users == 0:
            return 0.0
        
        completed_users = UserProgress.query.filter_by(
            module_id=self.id, 
            status=ModuleStatus.COMPLETED.value
        ).count()
        
        if total_users and total_users > 0:
            return (completed_users / total_users) * 100
        return 0.0
    
    @property
    def average_score(self) -> float:
        """Calculate average score for this module"""
        scores = db.session.query(UserProgress.score).filter_by(
            module_id=self.id,
            status=ModuleStatus.COMPLETED.value
        ).all()
        
        if not scores:
            return 0.0
        
        total_score = sum(score[0] for score in scores)
        if scores and len(scores) > 0:
            return total_score / len(scores)
        return 0.0
    
    def get_questions_by_set(self, question_set: int = 1) -> List['KnowledgeCheckQuestion']:
        """Get questions for a specific question set"""
        return self.knowledge_questions.filter_by(question_set=question_set).all()
    
    def get_random_questions(self, count: int = 5, question_set: int = 1) -> List['KnowledgeCheckQuestion']:
        """Get random questions for assessment"""
        import random
        questions = self.get_questions_by_set(question_set)
        if len(questions) <= count:
            return questions
        return random.sample(questions, count)
    
    def get_module_statistics(self) -> Dict[str, Any]:
        """Get comprehensive module statistics"""
        return {
            'module_id': self.id,
            'name': self.name,
            'order': self.order,
            'question_count': self.question_count,
            'completion_rate': self.completion_rate,
            'average_score': self.average_score,
            'has_simulation': self.has_simulation,
            'simulation_type': self.simulation_type,
            'total_attempts': self.user_progress.count(),
            'completed_attempts': self.user_progress.filter_by(status=ModuleStatus.COMPLETED.value).count()
        }
    
    @classmethod
    def get_by_order(cls, order: int):
        """Get module by order"""
        return cls.query.filter_by(order=order).first()
    
    @classmethod
    def get_all_ordered(cls) -> List['Module']:
        """Get all modules ordered by sequence"""
        return cls.query.order_by(cls.order).all()
    
    @classmethod
    def get_next_module(cls, current_order: int):
        """Get next module in sequence"""
        return cls.query.filter(cls.order > current_order).order_by(cls.order).first()
    
    @classmethod
    def get_previous_module(cls, current_order: int):
        """Get previous module in sequence"""
        return cls.query.filter(cls.order < current_order).order_by(cls.order.desc()).first()

class QuestionBase(BaseModel, TimestampMixin):
    """Base class for question models"""
    
    __abstract__ = True
    
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c', 'd'
    explanation = db.Column(db.Text, nullable=False)
    question_set = db.Column(db.Integer, default=1)
    
    def __init__(self, **kwargs):
        """Initialize question with validation"""
        if 'correct_answer' in kwargs:
            answer = kwargs['correct_answer'].lower()
            if answer not in ['a', 'b', 'c', 'd']:
                raise ValueError("Correct answer must be 'a', 'b', 'c', or 'd'")
            kwargs['correct_answer'] = answer
        super().__init__(**kwargs)
    
    def check_answer(self, user_answer: str) -> bool:
        """Check if user answer is correct"""
        return user_answer.lower() == self.correct_answer.lower()
    
    def get_options_dict(self) -> Dict[str, str]:
        """Get options as dictionary"""
        return {
            'a': self.option_a,
            'b': self.option_b,
            'c': self.option_c,
            'd': self.option_d
        }
    
    def get_correct_option_text(self) -> str:
        """Get the text of the correct option"""
        options = self.get_options_dict()
        return options.get(self.correct_answer, '')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert question to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'options': self.get_options_dict(),
            'correct_option_text': self.get_correct_option_text()
        })
        return base_dict

class KnowledgeCheckQuestion(QuestionBase):
    """Knowledge check question model for module assessments"""
    
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    
    @classmethod
    def get_by_module_and_set(cls, module_id: int, question_set: int = 1) -> List['KnowledgeCheckQuestion']:
        """Get questions by module and question set"""
        return cls.query.filter_by(module_id=module_id, question_set=question_set).all()
    
    @classmethod
    def get_random_by_module(cls, module_id: int, count: int = 5, question_set: int = 1) -> List['KnowledgeCheckQuestion']:
        """Get random questions for a module"""
        import random
        questions = cls.get_by_module_and_set(module_id, question_set)
        if len(questions) <= count:
            return questions
        return random.sample(questions, count)

class FinalAssessmentQuestion(QuestionBase):
    """Final assessment question model"""
    
    @classmethod
    def get_by_set(cls, question_set: int = 1) -> List['FinalAssessmentQuestion']:
        """Get questions by question set"""
        return cls.query.filter_by(question_set=question_set).all()
    
    @classmethod
    def get_random_questions(cls, count: int = 10, question_set: int = 1) -> List['FinalAssessmentQuestion']:
        """Get random questions for final assessment"""
        import random
        questions = cls.get_by_set(question_set)
        if len(questions) <= count:
            return questions
        return random.sample(questions, count)

