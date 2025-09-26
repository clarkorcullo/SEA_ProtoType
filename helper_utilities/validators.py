"""
Validators for input validation and data verification
"""

import re
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

class Validator(ABC):
    """Abstract base class for validators"""
    
    @abstractmethod
    def validate(self, value: Any) -> bool:
        """Validate the given value"""
        pass
    
    @abstractmethod
    def get_error_message(self) -> str:
        """Get error message for validation failure"""
        pass

class EmailValidator(Validator):
    """Email format validator"""
    
    def __init__(self):
        self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.error_message = "Invalid email format"
    
    def validate(self, value: str) -> bool:
        """Validate email format"""
        if not value or not isinstance(value, str):
            return False
        return re.match(self.pattern, value) is not None
    
    def get_error_message(self) -> str:
        return self.error_message

class PasswordValidator(Validator):
    """Password strength validator"""
    
    def __init__(self, min_length: int = 8):
        self.min_length = min_length
        self.error_message = f"Password must be at least {min_length} characters long and contain uppercase, lowercase, and numeric characters"
    
    def validate(self, value: str) -> bool:
        """Validate password strength"""
        if not value or not isinstance(value, str):
            return False
        
        if len(value) < self.min_length:
            return False
        
        if not re.search(r'[A-Z]', value):
            return False
        
        if not re.search(r'[a-z]', value):
            return False
        
        if not re.search(r'\d', value):
            return False
        
        return True
    
    def get_error_message(self) -> str:
        return self.error_message

class InputValidator:
    """Comprehensive input validator"""
    
    def __init__(self):
        self.email_validator = EmailValidator()
        self.password_validator = PasswordValidator()
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate user registration data"""
        errors = {}
        
        # Required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'specialization', 'year_level']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                if 'required' not in errors:
                    errors['required'] = []
                errors['required'].append(f"Missing required field: {field}")
        
        # Email validation
        if 'email' in user_data and user_data['email']:
            if not self.email_validator.validate(user_data['email']):
                if 'email' not in errors:
                    errors['email'] = []
                errors['email'].append(self.email_validator.get_error_message())
        
        # Password validation
        if 'password' in user_data and user_data['password']:
            if not self.password_validator.validate(user_data['password']):
                if 'password' not in errors:
                    errors['password'] = []
                errors['password'].append(self.password_validator.get_error_message())
        
        # Username validation
        if 'username' in user_data and user_data['username']:
            if len(user_data['username']) < 3:
                if 'username' not in errors:
                    errors['username'] = []
                errors['username'].append("Username must be at least 3 characters long")
            
            if not re.match(r'^[a-zA-Z0-9_]+$', user_data['username']):
                if 'username' not in errors:
                    errors['username'] = []
                errors['username'].append("Username can only contain letters, numbers, and underscores")
        
        # Full name validation
        if 'full_name' in user_data and user_data['full_name']:
            if len(user_data['full_name']) < 2:
                if 'full_name' not in errors:
                    errors['full_name'] = []
                errors['full_name'].append("Full name must be at least 2 characters long")
        
        return errors
    
    def validate_assessment_answers(self, questions: List[Any], answers: Dict[str, str]) -> Dict[str, List[str]]:
        """Validate assessment answers"""
        errors = {}
        
        # Check if all questions have answers
        question_ids = {str(q.id) for q in questions}
        answer_ids = set(answers.keys())
        
        missing_answers = question_ids - answer_ids
        if missing_answers:
            errors['missing_answers'] = [f"Missing answers for questions: {', '.join(missing_answers)}"]
        
        # Validate answer format
        valid_options = {'a', 'b', 'c', 'd'}
        invalid_answers = []
        for question_id, answer in answers.items():
            if answer.lower() not in valid_options:
                invalid_answers.append(f"Question {question_id}: Invalid answer '{answer}'")
        
        if invalid_answers:
            errors['invalid_answers'] = invalid_answers
        
        return errors
    
    def validate_simulation_answers(self, simulation_data: Dict[str, Any], answers: Dict[str, str]) -> Dict[str, List[str]]:
        """Validate simulation answers"""
        errors = {}
        
        options = simulation_data.get('options', [])
        option_ids = {str(option['id']) for option in options}
        answer_ids = set(answers.keys())
        
        # Check if all questions have answers
        missing_answers = option_ids - answer_ids
        if missing_answers:
            errors['missing_answers'] = [f"Missing answers for questions: {', '.join(missing_answers)}"]
        
        # Validate answer format
        valid_options = {'a', 'b', 'c', 'd'}
        invalid_answers = []
        for question_id, answer in answers.items():
            if answer.lower() not in valid_options:
                invalid_answers.append(f"Question {question_id}: Invalid answer '{answer}'")
        
        if invalid_answers:
            errors['invalid_answers'] = invalid_answers
        
        return errors
    
    def validate_feedback_data(self, feedback_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate feedback survey data"""
        errors = {}
        
        # Rating validation
        if 'rating' not in feedback_data:
            errors['rating'] = ["Rating is required"]
        else:
            rating = feedback_data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                errors['rating'] = ["Rating must be between 1 and 5"]
        
        # Feedback text validation (optional)
        if 'feedback_text' in feedback_data and feedback_data['feedback_text']:
            if len(feedback_data['feedback_text']) > 1000:
                errors['feedback_text'] = ["Feedback text must be less than 1000 characters"]
        
        # Difficulty level validation (optional)
        if 'difficulty_level' in feedback_data and feedback_data['difficulty_level']:
            valid_levels = ['easy', 'medium', 'hard']
            if feedback_data['difficulty_level'].lower() not in valid_levels:
                errors['difficulty_level'] = [f"Difficulty level must be one of: {', '.join(valid_levels)}"]
        
        return errors
    
    def sanitize_input(self, value: str) -> str:
        """Sanitize user input"""
        if not value:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', str(value))
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    def validate_module_data(self, module_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate module data"""
        errors = {}
        
        # Required fields
        required_fields = ['name', 'description', 'content', 'order']
        for field in required_fields:
            if field not in module_data or not module_data[field]:
                if 'required' not in errors:
                    errors['required'] = []
                errors['required'].append(f"Missing required field: {field}")
        
        # Order validation
        if 'order' in module_data and module_data['order']:
            try:
                order = int(module_data['order'])
                if order < 1:
                    errors['order'] = ["Order must be a positive integer"]
            except (ValueError, TypeError):
                errors['order'] = ["Order must be a valid integer"]
        
        # Content length validation
        if 'content' in module_data and module_data['content']:
            if len(module_data['content']) < 10:
                errors['content'] = ["Content must be at least 10 characters long"]
        
        return errors
    
    def validate_question_data(self, question_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate question data"""
        errors = {}
        
        # Required fields
        required_fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation']
        for field in required_fields:
            if field not in question_data or not question_data[field]:
                if 'required' not in errors:
                    errors['required'] = []
                errors['required'].append(f"Missing required field: {field}")
        
        # Correct answer validation
        if 'correct_answer' in question_data and question_data['correct_answer']:
            valid_answers = ['a', 'b', 'c', 'd']
            if question_data['correct_answer'].lower() not in valid_answers:
                errors['correct_answer'] = [f"Correct answer must be one of: {', '.join(valid_answers)}"]
        
        # Question text length validation
        if 'question_text' in question_data and question_data['question_text']:
            if len(question_data['question_text']) < 10:
                errors['question_text'] = ["Question text must be at least 10 characters long"]
        
        # Options length validation
        for option in ['option_a', 'option_b', 'option_c', 'option_d']:
            if option in question_data and question_data[option]:
                if len(question_data[option]) < 2:
                    if 'options' not in errors:
                        errors['options'] = []
                    errors['options'].append(f"{option} must be at least 2 characters long")
        
        return errors

