"""
Progress service for handling progress tracking business logic
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from data_models.progress_models import UserProgress, ProgressStatus, AssessmentResult, SimulationResult
from data_models.user_models import User
from data_models.content_models import Module

class ProgressService:
    """Service class for progress tracking operations"""
    
    def __init__(self):
        """Initialize progress service"""
        pass
    
    @staticmethod
    def get_user_overall_progress(user_id: int) -> Dict[str, Any]:
        """Get comprehensive user progress overview"""
        try:
            user = User.get_by_id(user_id)
            if not user:
                return {}
            
            # Get all user progress
            all_progress = UserProgress.get_user_progress(user_id)
            completed_progress = [p for p in all_progress if p.is_completed]
            
            # Get assessment results
            assessments = AssessmentResult.get_user_assessments(user_id)
            passed_assessments = [a for a in assessments if a.passed]
            
            # Get simulation results
            simulations = SimulationResult.get_user_simulations(user_id)
            completed_simulations = [s for s in simulations if s.completed]
            
            # Calculate statistics
            total_modules = Module.count()
            completion_percentage = (len(completed_progress) / total_modules) * 100 if total_modules > 0 else 0
            average_assessment_score = sum(a.score for a in assessments) / len(assessments) if assessments else 0
            average_simulation_score = sum(s.score for s in completed_simulations) / len(completed_simulations) if completed_simulations else 0
            
            return {
                'user_id': user_id,
                'total_modules': total_modules,
                'completed_modules': len(completed_progress),
                'completion_percentage': round(completion_percentage, 2),
                'total_assessments': len(assessments),
                'passed_assessments': len(passed_assessments),
                'average_assessment_score': round(average_assessment_score, 2),
                'total_simulations': len(simulations),
                'completed_simulations': len(completed_simulations),
                'average_simulation_score': round(average_simulation_score, 2),
                'total_time_spent': sum(p.time_spent for p in all_progress),
                'last_activity': max(p.updated_at for p in all_progress) if all_progress else None
            }
            
        except Exception as e:
            print(f"Error getting user overall progress: {e}")
            return {}
    
    @staticmethod
    def get_module_progress_details(user_id: int, module_id: int) -> Dict[str, Any]:
        """Get detailed progress for a specific module"""
        try:
            module = Module.get_by_id(module_id)
            if not module:
                return {}
            
            progress = UserProgress.get_module_progress(user_id, module_id)
            if not progress:
                return {
                    'module_id': module_id,
                    'module_name': module.name,
                    'status': ProgressStatus.NOT_STARTED.value,
                    'score': 0,
                    'attempts': 0,
                    'time_spent': 0,
                    'is_completed': False
                }
            
            # Get assessment results for this module
            assessments = AssessmentResult.get_user_assessments(
                user_id, 
                assessment_type='knowledge_check'
            )
            module_assessments = [a for a in assessments if a.module_id == module_id]
            
            return {
                'module_id': module_id,
                'module_name': module.name,
                'status': progress.status,
                'score': progress.score,
                'attempts': progress.attempts,
                'time_spent': progress.time_spent,
                'completed_at': progress.completed_at,
                'is_completed': progress.is_completed,
                'completion_time': progress.completion_time,
                'assessment_count': len(module_assessments),
                'best_assessment_score': max(a.score for a in module_assessments) if module_assessments else 0
            }
            
        except Exception as e:
            print(f"Error getting module progress details: {e}")
            return {}
    
    @staticmethod
    def update_progress_time(user_id: int, module_id: int, minutes: int) -> bool:
        """Update time spent on a module"""
        try:
            progress = UserProgress.get_module_progress(user_id, module_id)
            if not progress:
                progress = UserProgress(
                    user_id=user_id,
                    module_id=module_id,
                    status=ProgressStatus.IN_PROGRESS.value
                )
                progress.save()
            
            return progress.update_time_spent(minutes)
            
        except Exception as e:
            print(f"Error updating progress time: {e}")
            return False
    
    @staticmethod
    def get_learning_path_progress(user_id: int) -> List[Dict[str, Any]]:
        """Get progress for the entire learning path"""
        try:
            modules = Module.get_all_ordered()
            learning_path = []
            
            for module in modules:
                progress = UserProgress.get_module_progress(user_id, module.id)
                
                module_info = {
                    'module_id': module.id,
                    'module_name': module.name,
                    'module_order': module.order,
                    'has_simulation': module.has_simulation,
                    'simulation_type': module.simulation_type,
                    'status': progress.status if progress else ProgressStatus.NOT_STARTED.value,
                    'score': progress.score if progress else 0,
                    'attempts': progress.attempts if progress else 0,
                    'time_spent': progress.time_spent if progress else 0,
                    'is_completed': progress.is_completed if progress else False,
                    'completion_percentage': module.completion_rate,
                    'average_score': module.average_score
                }
                
                learning_path.append(module_info)
            
            return learning_path
            
        except Exception as e:
            print(f"Error getting learning path progress: {e}")
            return []
    
    @staticmethod
    def get_recent_activity(user_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent user activity"""
        try:
            recent_date = datetime.utcnow() - timedelta(days=days)
            
            # Get recent progress updates
            recent_progress = UserProgress.query.filter(
                UserProgress.user_id == user_id,
                UserProgress.updated_at >= recent_date
            ).order_by(UserProgress.updated_at.desc()).all()
            
            # Get recent assessments
            recent_assessments = AssessmentResult.query.filter(
                AssessmentResult.user_id == user_id,
                AssessmentResult.created_at >= recent_date
            ).order_by(AssessmentResult.created_at.desc()).all()
            
            # Get recent simulations
            recent_simulations = SimulationResult.query.filter(
                SimulationResult.user_id == user_id,
                SimulationResult.created_at >= recent_date
            ).order_by(SimulationResult.created_at.desc()).all()
            
            # Combine and sort activities
            activities = []
            
            for progress in recent_progress:
                activities.append({
                    'type': 'progress',
                    'action': f"Updated progress for Module {progress.module_id}",
                    'timestamp': progress.updated_at,
                    'details': {
                        'status': progress.status,
                        'score': progress.score,
                        'time_spent': progress.time_spent
                    }
                })
            
            for assessment in recent_assessments:
                activities.append({
                    'type': 'assessment',
                    'action': f"Completed {assessment.assessment_type} assessment",
                    'timestamp': assessment.created_at,
                    'details': {
                        'score': assessment.score,
                        'percentage': assessment.percentage_score,
                        'passed': assessment.passed
                    }
                })
            
            for simulation in recent_simulations:
                activities.append({
                    'type': 'simulation',
                    'action': f"Completed {simulation.simulation_type} simulation",
                    'timestamp': simulation.created_at,
                    'details': {
                        'score': simulation.score,
                        'completed': simulation.completed
                    }
                })
            
            # Sort by timestamp
            activities.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return activities
            
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
    
    @staticmethod
    def get_achievement_progress(user_id: int) -> Dict[str, Any]:
        """Get user achievement progress"""
        try:
            user = User.get_by_id(user_id)
            if not user:
                return {}
            
            # Get all progress data
            all_progress = UserProgress.get_user_progress(user_id)
            assessments = AssessmentResult.get_user_assessments(user_id)
            simulations = SimulationResult.get_user_simulations(user_id)
            
            # Define achievements
            achievements = {
                'first_module': {
                    'name': 'First Steps',
                    'description': 'Complete your first module',
                    'achieved': len([p for p in all_progress if p.is_completed]) >= 1,
                    'progress': min(len([p for p in all_progress if p.is_completed]), 1),
                    'target': 1
                },
                'half_way': {
                    'name': 'Halfway There',
                    'description': 'Complete 50% of all modules',
                    'achieved': len([p for p in all_progress if p.is_completed]) >= 4,
                    'progress': len([p for p in all_progress if p.is_completed]),
                    'target': 4
                },
                'perfect_score': {
                    'name': 'Perfect Score',
                    'description': 'Get 100% on any assessment',
                    'achieved': any(a.score == a.total_questions for a in assessments),
                    'progress': len([a for a in assessments if a.score == a.total_questions]),
                    'target': 1
                },
                'simulation_master': {
                    'name': 'Simulation Master',
                    'description': 'Complete all simulations',
                    'achieved': len([s for s in simulations if s.completed]) >= 3,
                    'progress': len([s for s in simulations if s.completed]),
                    'target': 3
                },
                'speed_learner': {
                    'name': 'Speed Learner',
                    'description': 'Complete a module in under 30 minutes',
                    'achieved': any(p.time_spent < 30 and p.is_completed for p in all_progress),
                    'progress': len([p for p in all_progress if p.time_spent < 30 and p.is_completed]),
                    'target': 1
                }
            }
            
            # Calculate overall achievement percentage
            total_achievements = len(achievements)
            achieved_count = sum(1 for a in achievements.values() if a['achieved'])
            achievement_percentage = (achieved_count / total_achievements) * 100
            
            return {
                'achievements': achievements,
                'total_achievements': total_achievements,
                'achieved_count': achieved_count,
                'achievement_percentage': round(achievement_percentage, 2)
            }
            
        except Exception as e:
            print(f"Error getting achievement progress: {e}")
            return {}
    
    @staticmethod
    def get_progress_analytics(user_id: int) -> Dict[str, Any]:
        """Get detailed progress analytics"""
        try:
            user = User.get_by_id(user_id)
            if not user:
                return {}
            
            # Get all progress data
            all_progress = UserProgress.get_user_progress(user_id)
            assessments = AssessmentResult.get_user_assessments(user_id)
            simulations = SimulationResult.get_user_simulations(user_id)
            
            # Time analysis
            total_time_spent = sum(p.time_spent for p in all_progress)
            average_time_per_module = total_time_spent / len(all_progress) if all_progress else 0
            
            # Score analysis
            assessment_scores = [a.score for a in assessments]
            simulation_scores = [s.score for s in simulations if s.completed]
            
            # Progress trends
            progress_by_date = {}
            for progress in all_progress:
                date = progress.updated_at.date()
                if date not in progress_by_date:
                    progress_by_date[date] = {'modules_started': 0, 'modules_completed': 0}
                
                if progress.status == ProgressStatus.IN_PROGRESS.value:
                    progress_by_date[date]['modules_started'] += 1
                elif progress.is_completed:
                    progress_by_date[date]['modules_completed'] += 1
            
            return {
                'time_analytics': {
                    'total_time_spent_minutes': total_time_spent,
                    'average_time_per_module': round(average_time_per_module, 2),
                    'total_time_spent_hours': round(total_time_spent / 60, 2)
                },
                'score_analytics': {
                    'assessment_scores': assessment_scores,
                    'simulation_scores': simulation_scores,
                    'average_assessment_score': round(sum(assessment_scores) / len(assessment_scores), 2) if assessment_scores else 0,
                    'average_simulation_score': round(sum(simulation_scores) / len(simulation_scores), 2) if simulation_scores else 0,
                    'best_assessment_score': max(assessment_scores) if assessment_scores else 0,
                    'best_simulation_score': max(simulation_scores) if simulation_scores else 0
                },
                'progress_trends': {
                    'progress_by_date': progress_by_date,
                    'total_days_active': len(progress_by_date),
                    'most_active_day': max(progress_by_date.items(), key=lambda x: sum(x[1].values()))[0] if progress_by_date else None
                }
            }
            
        except Exception as e:
            print(f"Error getting progress analytics: {e}")
            return {}

