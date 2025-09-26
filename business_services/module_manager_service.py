"""
Module Manager Service for handling module content and knowledge check rules
"""

from typing import List, Dict, Any, Optional
import random

# from learning_modules import (
#     Module1Content, Module1Questions,
#     Module2Content, Module2Questions,
#     Module3Content, Module3Questions,
#     Module4Content, Module4Questions,
#     Module5Content, Module5Questions,
#     FinalAssessmentContent, FinalAssessmentQuestions
# )

class ModuleManagerService:
    """Service for managing module content and knowledge check rules"""
    
    # Knowledge check rules
    KNOWLEDGE_CHECK_PASSING_THRESHOLD = 80.0  # 80% passing score
    KNOWLEDGE_CHECK_QUESTION_COUNT = 5  # 5 questions per knowledge check
    MAX_ATTEMPTS_PER_MODULE = 10  # Maximum attempts per module
    
    # Final assessment specific rules
    FINAL_ASSESSMENT_QUESTION_COUNT = 25  # 25 questions for final assessment
    FINAL_ASSESSMENT_PASSING_THRESHOLD = 80.0  # 80% passing score
    FINAL_ASSESSMENT_MAX_RETAKES = 3  # 3 retakes maximum
    FINAL_ASSESSMENT_COOLDOWN_HOURS = 48  # 48 hours cooldown between retake cycles
    
    @staticmethod
    def get_module_content(module_number: int) -> Optional[Dict[str, Any]]:
        """Get content for a specific module"""
        # Temporarily disabled - module content being rebuilt
        return {"error": "Module content being rebuilt"}
    
    @staticmethod
    def get_knowledge_check_questions(module_number: int, attempt_number: int = 1) -> List[Dict[str, Any]]:
        """Get knowledge check questions for a module with randomization"""
        # Temporarily disabled - module content being rebuilt
        return []
    
    @staticmethod
    def grade_knowledge_check(questions: List[Dict[str, Any]], user_answers: Dict[str, str]) -> Dict[str, Any]:
        """Grade a knowledge check and return results"""
        try:
            total_questions = len(questions)
            correct_answers = 0
            detailed_results = []
            
            for question in questions:
                question_id = str(question.get('id', questions.index(question)))
                user_answer = user_answers.get(question_id, '').lower()
                correct_answer = question.get('correct_answer', '').lower()
                
                is_correct = user_answer == correct_answer
                if is_correct:
                    correct_answers += 1
                
                detailed_results.append({
                    'question_id': question_id,
                    'question_text': question.get('question_text', ''),
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'explanation': question.get('explanation', '')
                })
            
            score = correct_answers
            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            passed = percentage >= ModuleManagerService.KNOWLEDGE_CHECK_PASSING_THRESHOLD
            
            return {
                'score': score,
                'total_questions': total_questions,
                'percentage': percentage,
                'passed': passed,
                'detailed_results': detailed_results,
                'passing_threshold': ModuleManagerService.KNOWLEDGE_CHECK_PASSING_THRESHOLD
            }
            
        except Exception as e:
            print(f"Error grading knowledge check: {e}")
            return {
                'score': 0,
                'total_questions': 0,
                'percentage': 0,
                'passed': False,
                'detailed_results': [],
                'passing_threshold': ModuleManagerService.KNOWLEDGE_CHECK_PASSING_THRESHOLD
            }
    
    @staticmethod
    def can_retake_knowledge_check(module_number: int, user_id: int, current_attempts: int, last_attempt_time: str = None) -> Dict[str, Any]:
        """Check if user can retake knowledge check"""
        if module_number == 6:  # Final Assessment (now module 6)
            return ModuleManagerService._can_retake_final_assessment(current_attempts, last_attempt_time)
        else:
            # Regular modules: unlimited retakes with limit to prevent abuse
            return {
                'can_retake': current_attempts < ModuleManagerService.MAX_ATTEMPTS_PER_MODULE,
                'reason': 'Regular module retake policy',
                'attempts_remaining': ModuleManagerService.MAX_ATTEMPTS_PER_MODULE - current_attempts
            }
    
    @staticmethod
    def _can_retake_final_assessment(current_attempts: int, last_attempt_time: str = None) -> Dict[str, Any]:
        """Check if user can retake final assessment (3 attempts every 48 hours)"""
        from datetime import datetime, timedelta
        
        if current_attempts < ModuleManagerService.FINAL_ASSESSMENT_MAX_RETAKES:
            return {
                'can_retake': True,
                'reason': f'Attempt {current_attempts + 1} of {ModuleManagerService.FINAL_ASSESSMENT_MAX_RETAKES}',
                'attempts_remaining': ModuleManagerService.FINAL_ASSESSMENT_MAX_RETAKES - current_attempts
            }
        
        # Check if 48 hours have passed since last attempt
        if last_attempt_time:
            try:
                last_attempt = datetime.fromisoformat(last_attempt_time.replace('Z', '+00:00'))
                current_time = datetime.now(last_attempt.tzinfo)
                time_diff = current_time - last_attempt
                
                if time_diff.total_seconds() >= ModuleManagerService.FINAL_ASSESSMENT_COOLDOWN_HOURS * 3600:
                    return {
                        'can_retake': True,
                        'reason': '48-hour cooldown period completed',
                        'attempts_remaining': ModuleManagerService.FINAL_ASSESSMENT_MAX_RETAKES,
                        'cooldown_reset': True
                    }
                else:
                    remaining_hours = ModuleManagerService.FINAL_ASSESSMENT_COOLDOWN_HOURS - (time_diff.total_seconds() / 3600)
                    return {
                        'can_retake': False,
                        'reason': f'48-hour cooldown period active. {remaining_hours:.1f} hours remaining',
                        'attempts_remaining': 0,
                        'cooldown_remaining_hours': remaining_hours
                    }
            except Exception as e:
                print(f"Error parsing last attempt time: {e}")
        
        return {
            'can_retake': False,
            'reason': 'Maximum attempts reached. Wait 48 hours to retry.',
            'attempts_remaining': 0
        }
    
    @staticmethod
    def get_next_question_set(module_number: int, current_attempt: int) -> int:
        """Get the next question set for retakes"""
        # Cycle through question sets for retakes
        return (current_attempt % 3) + 1
    
    @staticmethod
    def validate_knowledge_check_answers(questions: List[Dict[str, Any]], answers: Dict[str, str]) -> Dict[str, List[str]]:
        """Validate knowledge check answers"""
        errors = {}
        
        # Check if all questions have answers
        question_ids = {str(q.get('id', questions.index(q))) for q in questions}
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
    
    @staticmethod
    def get_module_progress_summary(user_id: int, module_number: int) -> Dict[str, Any]:
        """Get progress summary for a specific module"""
        # This would integrate with the progress tracking system
        # For now, return basic structure
        return {
            'module_number': module_number,
            'user_id': user_id,
            'attempts': 0,
            'best_score': 0,
            'passed': False,
            'last_attempt_date': None,
            'can_retake': True
        }
    
    @staticmethod
    def get_all_modules_info() -> List[Dict[str, Any]]:
        """Get information about all modules"""
        modules_info = []
        
        for module_num in range(1, 6):  # Modules 1-5
            content = ModuleManagerService.get_module_content(module_num)
            if content:
                modules_info.append({
                    'module_number': module_num,
                    'title': content.get('title', f'Module {module_num}'),
                    'description': content.get('description', ''),
                    'estimated_time': content.get('estimated_time', 30),
                    'difficulty_level': content.get('difficulty_level', 'intermediate'),
                    'is_final_assessment': module_num == 6
                })
        
        return modules_info
    
    @staticmethod
    def get_knowledge_check_rules() -> Dict[str, Any]:
        """Get knowledge check rules and requirements"""
        return {
            'passing_threshold': ModuleManagerService.KNOWLEDGE_CHECK_PASSING_THRESHOLD,
            'question_count': ModuleManagerService.KNOWLEDGE_CHECK_QUESTION_COUNT,
            'max_attempts': ModuleManagerService.MAX_ATTEMPTS_PER_MODULE,
            'retake_policy': 'Unlimited retakes with 80% passing threshold',
            'randomization': 'Questions are randomized for each attempt',
            'question_sets': 'Multiple question sets available for retakes'
        }
    
    @staticmethod
    def get_final_assessment_rules() -> Dict[str, Any]:
        """Get final assessment specific rules and requirements"""
        return {
            'question_count': ModuleManagerService.FINAL_ASSESSMENT_QUESTION_COUNT,
            'passing_threshold': ModuleManagerService.FINAL_ASSESSMENT_PASSING_THRESHOLD,
            'max_retakes': ModuleManagerService.FINAL_ASSESSMENT_MAX_RETAKES,
            'cooldown_hours': ModuleManagerService.FINAL_ASSESSMENT_COOLDOWN_HOURS,
            'retake_policy': '3 attempts every 48 hours',
            'randomization': 'Different question sets for each retake',
            'no_repeat_questions': 'Questions will not repeat from previous attempts',
            'satisfaction_survey_required': True,
            'certification_requirement': 'Survey completion mandatory for certificate'
        }
    
    @staticmethod
    def can_generate_certificate(user_id: int, final_assessment_passed: bool, survey_completed: bool) -> Dict[str, Any]:
        """Check if user can generate certificate after final assessment"""
        if not final_assessment_passed:
            return {
                'can_generate': False,
                'reason': 'Final assessment not passed',
                'requirements_met': False
            }
        
        if not survey_completed:
            return {
                'can_generate': False,
                'reason': 'Satisfaction survey not completed',
                'requirements_met': False,
                'missing_requirement': 'survey'
            }
        
        return {
            'can_generate': True,
            'reason': 'All requirements met',
            'requirements_met': True
        }
    
    @staticmethod
    def get_question_randomization_info(module_number: int, attempt_number: int) -> Dict[str, Any]:
        """Get information about question randomization for retakes"""
        if module_number == 6:  # Final Assessment (now module 6)
            return {
                'module_type': 'final_assessment',
                'question_count': ModuleManagerService.FINAL_ASSESSMENT_QUESTION_COUNT,
                'question_sets_available': 3,
                'current_set': ((attempt_number - 1) % 3) + 1,
                'randomization_type': 'Different question set for each retake',
                'no_repeat_policy': 'Questions will not repeat from previous attempts'
            }
        else:
            return {
                'module_type': 'regular_module',
                'question_count': ModuleManagerService.KNOWLEDGE_CHECK_QUESTION_COUNT,
                'question_sets_available': 3,
                'current_set': ((attempt_number - 1) % 3) + 1,
                'randomization_type': 'Random selection from question set',
                'retake_policy': 'Unlimited retakes with different question sets'
            }
