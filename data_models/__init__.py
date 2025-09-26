"""
Models package for Social Engineering Awareness Program
Contains all database models with proper inheritance and OOP structure
"""

from .base_models import BaseModel, TimestampMixin
from .user_models import User, PasswordResetToken
from .content_models import Module, KnowledgeCheckQuestion, FinalAssessmentQuestion
from .progress_models import UserProgress, AssessmentResult, SimulationResult, FeedbackSurvey

__all__ = [
    'BaseModel',
    'TimestampMixin', 
    'User',
    'PasswordResetToken',
    'Module',
    'KnowledgeCheckQuestion',
    'FinalAssessmentQuestion',
    'UserProgress',
    'AssessmentResult',
    'SimulationResult',
    'FeedbackSurvey'
]

