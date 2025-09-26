"""
Assessment service for handling assessment-related business logic
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import random

from data_models.content_models import KnowledgeCheckQuestion, FinalAssessmentQuestion
from data_models.progress_models import AssessmentResult, AssessmentType
from data_models.user_models import User

class AssessmentService:
    """Service class for assessment operations"""
    
    def __init__(self):
        """Initialize assessment service"""
        pass
    
    @staticmethod
    def create_knowledge_check(module_id: int, question_count: int = 5, question_set: int = 1) -> List[KnowledgeCheckQuestion]:
        """Create a knowledge check assessment for a module"""
        try:
            questions = KnowledgeCheckQuestion.get_random_by_module(
                module_id=module_id,
                count=question_count,
                question_set=question_set
            )
            return questions
        except Exception as e:
            print(f"Error creating knowledge check: {e}")
            return []
    
    @staticmethod
    def create_final_assessment(question_count: int = 25, question_set: int = 1) -> List[KnowledgeCheckQuestion]:
        """Create a final assessment using final assessment questions"""
        try:
            questions = FinalAssessmentQuestion.get_random_questions(
                count=question_count,
                question_set=question_set
            )
            return questions
        except Exception as e:
            print(f"Error creating final assessment: {e}")
            return []
    
    @staticmethod
    def grade_assessment(questions: List, user_answers: Dict[str, str]) -> Tuple[int, int, float, Dict[str, Any]]:
        """Grade an assessment and return results"""
        try:
            total_questions = len(questions)
            correct_answers = 0
            detailed_results = []
            
            for question in questions:
                question_id = str(question.id)
                user_answer = user_answers.get(question_id, '').lower()
                is_correct = question.check_answer(user_answer)
                
                if is_correct:
                    correct_answers += 1
                
                detailed_results.append({
                    'question_id': question.id,
                    'question_text': question.question_text,
                    'user_answer': user_answer,
                    'correct_answer': question.correct_answer,
                    'is_correct': is_correct,
                    'explanation': question.explanation
                })
            
            score = correct_answers
            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            
            return score, total_questions, percentage, detailed_results
            
        except Exception as e:
            print(f"Error grading assessment: {e}")
            return 0, 0, 0.0, []
    
    @staticmethod
    def save_assessment_result(
        user_id: int,
        assessment_type: str,
        score: int,
        total_questions: int,
        correct_answers: int,
        time_taken: int = 0,
        module_id: Optional[int] = None,
        answers_data: Optional[Dict[str, Any]] = None
    ) -> Optional[AssessmentResult]:
        """Save assessment result to database"""
        try:
            # Validate assessment type
            if assessment_type not in [e.value for e in AssessmentType]:
                raise ValueError(f"Invalid assessment type: {assessment_type}")
            
            # Create assessment result
            result = AssessmentResult(
                user_id=user_id,
                assessment_type=assessment_type,
                module_id=module_id,
                score=score,
                total_questions=total_questions,
                correct_answers=correct_answers,
                time_taken=time_taken
            )
            
            # Set answers data if provided
            if answers_data:
                result.set_answers_data(answers_data)
            
            # Calculate pass status
            result.calculate_pass_status()
            
            # Save to database
            if result.save():
                return result
            return None
            
        except Exception as e:
            print(f"Error saving assessment result: {e}")
            return None
    
    @staticmethod
    def get_user_assessment_history(user_id: int, assessment_type: Optional[str] = None) -> List[AssessmentResult]:
        """Get user's assessment history"""
        try:
            return AssessmentResult.get_user_assessments(user_id, assessment_type)
        except Exception as e:
            print(f"Error getting assessment history: {e}")
            return []
    
    @staticmethod
    def get_user_best_score(user_id: int, assessment_type: str) -> Optional[AssessmentResult]:
        """Get user's best score for a specific assessment type"""
        try:
            return AssessmentResult.get_best_score(user_id, assessment_type)
        except Exception as e:
            print(f"Error getting best score: {e}")
            return None
    
    @staticmethod
    def get_assessment_statistics(assessment_type: str) -> Dict[str, Any]:
        """Get statistics for a specific assessment type"""
        try:
            # Get all results for this assessment type
            results = AssessmentResult.query.filter_by(assessment_type=assessment_type).all()
            
            if not results:
                return {
                    'total_attempts': 0,
                    'average_score': 0.0,
                    'pass_rate': 0.0,
                    'best_score': 0,
                    'total_participants': 0
                }
            
            total_attempts = len(results)
            total_participants = len(set(r.user_id for r in results))
            average_score = sum(r.score for r in results) / total_attempts if total_attempts and total_attempts > 0 else 0
            pass_rate = (len([r for r in results if r.passed]) / total_attempts) * 100 if total_attempts and total_attempts > 0 else 0
            best_score = max(r.score for r in results)
            
            return {
                'total_attempts': total_attempts,
                'average_score': round(average_score, 2),
                'pass_rate': round(pass_rate, 2),
                'best_score': best_score,
                'total_participants': total_participants
            }
            
        except Exception as e:
            print(f"Error getting assessment statistics: {e}")
            return {}
    
    @staticmethod
    def get_user_progress_comparison(user_id: int) -> Dict[str, Any]:
        """Compare user's progress across different assessment types"""
        try:
            user = User.get_by_id(user_id)
            if not user:
                return {}
            
            comparison = {}
            
            for assessment_type in AssessmentType:
                best_result = AssessmentResult.get_best_score(user_id, assessment_type.value)
                if best_result:
                    comparison[assessment_type.value] = {
                        'best_score': best_result.score,
                        'percentage': best_result.percentage_score,
                        'passed': best_result.passed,
                        'attempts': len(AssessmentResult.get_user_assessments(user_id, assessment_type.value))
                    }
                else:
                    comparison[assessment_type.value] = {
                        'best_score': 0,
                        'percentage': 0.0,
                        'passed': False,
                        'attempts': 0
                    }
            
            return comparison
            
        except Exception as e:
            print(f"Error getting progress comparison: {e}")
            return {}
    
    @staticmethod
    def validate_assessment_answers(questions: List, answers: Dict[str, str]) -> bool:
        """Validate that all questions have answers"""
        try:
            question_ids = {str(q.id) for q in questions}
            answer_ids = set(answers.keys())
            
            # Check if all questions have answers
            missing_answers = question_ids - answer_ids
            if missing_answers:
                print(f"Missing answers for questions: {missing_answers}")
                return False
            
            # Check if all answers are valid
            valid_options = {'a', 'b', 'c', 'd'}
            for answer in answers.values():
                if answer.lower() not in valid_options:
                    print(f"Invalid answer option: {answer}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error validating assessment answers: {e}")
            return False
    
    @staticmethod
    def get_assessment_questions_by_type(assessment_type: str, **kwargs) -> List:
        """Get questions based on assessment type"""
        try:
            if assessment_type == AssessmentType.KNOWLEDGE_CHECK.value:
                module_id = kwargs.get('module_id')
                question_count = kwargs.get('question_count', 5)
                question_set = kwargs.get('question_set', 1)
                
                if not module_id:
                    raise ValueError("Module ID is required for knowledge check")
                
                return AssessmentService.create_knowledge_check(
                    module_id=module_id,
                    question_count=question_count,
                    question_set=question_set
                )
            
            elif assessment_type == AssessmentType.FINAL_ASSESSMENT.value:
                question_count = kwargs.get('question_count', 10)
                question_set = kwargs.get('question_set', 1)
                
                return AssessmentService.create_final_assessment(
                    question_count=question_count,
                    question_set=question_set
                )
            
            else:
                raise ValueError(f"Unsupported assessment type: {assessment_type}")
                
        except Exception as e:
            print(f"Error getting assessment questions: {e}")
            return []

