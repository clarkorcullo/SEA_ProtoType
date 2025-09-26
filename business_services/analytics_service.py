"""
Analytics service for handling data analysis and reporting
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from data_models.user_models import User
from data_models.content_models import Module
from data_models.progress_models import UserProgress, AssessmentResult, SimulationResult, FeedbackSurvey

class AnalyticsService:
    """Service class for analytics and reporting operations"""
    
    def __init__(self):
        """Initialize analytics service"""
        pass
    
    @staticmethod
    def get_system_overview() -> Dict[str, Any]:
        """Get comprehensive system overview statistics"""
        try:
            # User statistics
            total_users = User.count()
            active_users = User.query.filter(
                User.updated_at >= datetime.utcnow() - timedelta(days=30)
            ).count()
            
            # Module statistics
            total_modules = Module.count()
            modules_with_simulations = Module.query.filter_by(has_simulation=True).count()
            
            # Progress statistics
            total_progress_records = UserProgress.count()
            completed_progress = UserProgress.query.filter_by(status='completed').count()
            
            # Assessment statistics
            total_assessments = AssessmentResult.count()
            passed_assessments = AssessmentResult.query.filter_by(passed=True).count()
            
            # Simulation statistics
            total_simulations = SimulationResult.count()
            completed_simulations = SimulationResult.query.filter_by(completed=True).count()
            
            # Feedback statistics
            total_feedback = FeedbackSurvey.count()
            average_rating = FeedbackSurvey.get_average_rating()
            
            return {
                'users': {
                    'total_users': total_users,
                    'active_users': active_users,
                    'active_percentage': round((active_users / total_users) * 100, 2) if total_users > 0 else 0
                },
                'modules': {
                    'total_modules': total_modules,
                    'modules_with_simulations': modules_with_simulations,
                    'simulation_percentage': round((modules_with_simulations / total_modules) * 100, 2) if total_modules > 0 else 0
                },
                'progress': {
                    'total_progress_records': total_progress_records,
                    'completed_progress': completed_progress,
                    'completion_rate': round((completed_progress / total_progress_records) * 100, 2) if total_progress_records > 0 else 0
                },
                'assessments': {
                    'total_assessments': total_assessments,
                    'passed_assessments': passed_assessments,
                    'pass_rate': round((passed_assessments / total_assessments) * 100, 2) if total_assessments > 0 else 0
                },
                'simulations': {
                    'total_simulations': total_simulations,
                    'completed_simulations': completed_simulations,
                    'completion_rate': round((completed_simulations / total_simulations) * 100, 2) if total_simulations > 0 else 0
                },
                'feedback': {
                    'total_feedback': total_feedback,
                    'average_rating': round(average_rating, 2)
                }
            }
            
        except Exception as e:
            print(f"Error getting system overview: {e}")
            return {}
    
    @staticmethod
    def get_user_performance_analytics() -> Dict[str, Any]:
        """Get user performance analytics"""
        try:
            # Get all users with their performance data
            users = User.get_all()
            
            performance_data = {
                'total_users': len(users),
                'performance_distribution': {
                    'excellent': 0,  # 90-100%
                    'good': 0,       # 70-89%
                    'average': 0,    # 50-69%
                    'below_average': 0  # <50%
                },
                'completion_distribution': {
                    'completed_all': 0,
                    'completed_half': 0,
                    'completed_some': 0,
                    'not_started': 0
                },
                'average_scores': {
                    'assessment_score': 0,
                    'simulation_score': 0,
                    'completion_percentage': 0
                }
            }
            
            total_assessment_score = 0
            total_simulation_score = 0
            total_completion_percentage = 0
            valid_users = 0
            
            for user in users:
                # Get user statistics
                user_stats = user.get_progress_summary()
                
                if user_stats['total_assessments'] > 0:
                    total_assessment_score += user_stats['average_score']
                    total_simulation_score += user_stats.get('simulation_statistics', {}).get('average_score', 0)
                    total_completion_percentage += user_stats['completion_percentage']
                    valid_users += 1
                
                # Categorize performance
                completion_percentage = user_stats['completion_percentage']
                if completion_percentage >= 90:
                    performance_data['performance_distribution']['excellent'] += 1
                elif completion_percentage >= 70:
                    performance_data['performance_distribution']['good'] += 1
                elif completion_percentage >= 50:
                    performance_data['performance_distribution']['average'] += 1
                else:
                    performance_data['performance_distribution']['below_average'] += 1
                
                # Categorize completion
                modules_completed = user_stats['modules_completed']
                if modules_completed >= 5:
                    performance_data['completion_distribution']['completed_all'] += 1
                elif modules_completed >= 4:
                    performance_data['completion_distribution']['completed_half'] += 1
                elif modules_completed > 0:
                    performance_data['completion_distribution']['completed_some'] += 1
                else:
                    performance_data['completion_distribution']['not_started'] += 1
            
            # Calculate averages
            if valid_users > 0:
                performance_data['average_scores']['assessment_score'] = round(total_assessment_score / valid_users, 2)
                performance_data['average_scores']['simulation_score'] = round(total_simulation_score / valid_users, 2)
                performance_data['average_scores']['completion_percentage'] = round(total_completion_percentage / valid_users, 2)
            
            return performance_data
            
        except Exception as e:
            print(f"Error getting user performance analytics: {e}")
            return {}
    
    @staticmethod
    def get_module_analytics() -> List[Dict[str, Any]]:
        """Get analytics for each module"""
        try:
            modules = Module.get_all_ordered()
            module_analytics = []
            
            for module in modules:
                # Get module statistics
                module_stats = module.get_module_statistics()
                
                # Get assessment statistics for this module
                module_assessments = AssessmentResult.query.filter_by(
                    module_id=module.id,
                    assessment_type='knowledge_check'
                ).all()
                
                assessment_stats = {
                    'total_attempts': len(module_assessments),
                    'passed_attempts': len([a for a in module_assessments if a.passed]),
                    'average_score': sum(a.score for a in module_assessments) / len(module_assessments) if module_assessments and len(module_assessments) > 0 else 0,
                    'best_score': max(a.score for a in module_assessments) if module_assessments else 0
                }
                
                # Get feedback for this module
                module_feedback = FeedbackSurvey.get_module_feedback(module.id)
                feedback_stats = {
                    'total_feedback': len(module_feedback),
                    'average_rating': FeedbackSurvey.get_average_rating(module.id),
                    'rating_distribution': FeedbackSurvey.get_rating_distribution(module.id)
                }
                
                module_analytics.append({
                    'module_id': module.id,
                    'module_name': module.name,
                    'module_order': module.order,
                    'module_stats': module_stats,
                    'assessment_stats': assessment_stats,
                    'feedback_stats': feedback_stats
                })
            
            return module_analytics
            
        except Exception as e:
            print(f"Error getting module analytics: {e}")
            return []
    
    @staticmethod
    def get_trend_analytics(days: int = 30) -> Dict[str, Any]:
        """Get trend analytics over time"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Daily user registrations
            daily_registrations = defaultdict(int)
            new_users = User.query.filter(User.created_at >= start_date).all()
            
            for user in new_users:
                date = user.created_at.date()
                daily_registrations[date] += 1
            
            # Daily progress completions
            daily_completions = defaultdict(int)
            recent_progress = UserProgress.query.filter(
                UserProgress.completed_at >= start_date
            ).all()
            
            for progress in recent_progress:
                date = progress.completed_at.date()
                daily_completions[date] += 1
            
            # Daily assessment completions
            daily_assessments = defaultdict(int)
            recent_assessments = AssessmentResult.query.filter(
                AssessmentResult.created_at >= start_date
            ).all()
            
            for assessment in recent_assessments:
                date = assessment.created_at.date()
                daily_assessments[date] += 1
            
            # Daily simulation completions
            daily_simulations = defaultdict(int)
            recent_simulations = SimulationResult.query.filter(
                SimulationResult.created_at >= start_date
            ).all()
            
            for simulation in recent_simulations:
                date = simulation.created_at.date()
                daily_simulations[date] += 1
            
            return {
                'daily_registrations': dict(daily_registrations),
                'daily_completions': dict(daily_completions),
                'daily_assessments': dict(daily_assessments),
                'daily_simulations': dict(daily_simulations),
                'total_days': days
            }
            
        except Exception as e:
            print(f"Error getting trend analytics: {e}")
            return {}
    
    @staticmethod
    def get_assessment_analytics() -> Dict[str, Any]:
        """Get comprehensive assessment analytics"""
        try:
            # Get all assessment results
            all_assessments = AssessmentResult.get_all()
            
            # Group by assessment type
            assessment_types = defaultdict(list)
            for assessment in all_assessments:
                assessment_types[assessment.assessment_type].append(assessment)
            
            analytics = {}
            
            for assessment_type, assessments in assessment_types.items():
                if not assessments:
                    continue
                
                total_attempts = len(assessments)
                passed_attempts = len([a for a in assessments if a.passed])
                average_score = sum(a.score for a in assessments) / total_attempts if total_attempts and total_attempts > 0 else 0
                best_score = max(a.score for a in assessments) if assessments else 0
                average_time = sum(a.time_taken_minutes for a in assessments) / total_attempts if total_attempts and total_attempts > 0 else 0
                
                # Score distribution
                score_distribution = {
                    '90-100': len([a for a in assessments if a.percentage_score >= 90]),
                    '80-89': len([a for a in assessments if 80 <= a.percentage_score < 90]),
                    '70-79': len([a for a in assessments if 70 <= a.percentage_score < 80]),
                    '60-69': len([a for a in assessments if 60 <= a.percentage_score < 70]),
                    '50-59': len([a for a in assessments if 50 <= a.percentage_score < 60]),
                    'below_50': len([a for a in assessments if a.percentage_score < 50])
                }
                
                analytics[assessment_type] = {
                    'total_attempts': total_attempts,
                    'passed_attempts': passed_attempts,
                    'pass_rate': round((passed_attempts / total_attempts) * 100, 2) if total_attempts and total_attempts > 0 else 0,
                    'average_score': round(average_score, 2),
                    'best_score': best_score,
                    'average_time_minutes': round(average_time, 2),
                    'score_distribution': score_distribution
                }
            
            return analytics
            
        except Exception as e:
            print(f"Error getting assessment analytics: {e}")
            return {}
    
    @staticmethod
    def get_simulation_analytics() -> Dict[str, Any]:
        """Get comprehensive simulation analytics"""
        try:
            # Get all simulation results
            all_simulations = SimulationResult.get_all()
            
            # Group by simulation type
            simulation_types = defaultdict(list)
            for simulation in all_simulations:
                simulation_types[simulation.simulation_type].append(simulation)
            
            analytics = {}
            
            for simulation_type, simulations in simulation_types.items():
                if not simulations:
                    continue
                
                total_attempts = len(simulations)
                completed_simulations = len([s for s in simulations if s.completed])
                average_score = sum(s.score for s in completed_simulations) / len(completed_simulations) if completed_simulations and len(completed_simulations) > 0 else 0
                best_score = max(s.score for s in simulations) if simulations else 0
                average_time = sum(s.time_taken_minutes for s in completed_simulations) / len(completed_simulations) if completed_simulations and len(completed_simulations) > 0 else 0
                
                analytics[simulation_type] = {
                    'total_attempts': total_attempts,
                    'completed_simulations': completed_simulations,
                    'completion_rate': round((completed_simulations / total_attempts) * 100, 2) if total_attempts and total_attempts > 0 else 0,
                    'average_score': round(average_score, 2),
                    'best_score': best_score,
                    'average_time_minutes': round(average_time, 2)
                }
            
            return analytics
            
        except Exception as e:
            print(f"Error getting simulation analytics: {e}")
            return {}
    
    @staticmethod
    def get_feedback_analytics() -> Dict[str, Any]:
        """Get feedback and satisfaction analytics"""
        try:
            # Get all feedback
            all_feedback = FeedbackSurvey.get_all()
            
            # Overall statistics
            total_feedback = len(all_feedback)
            average_rating = FeedbackSurvey.get_average_rating()
            rating_distribution = FeedbackSurvey.get_rating_distribution()
            
            # Module-specific feedback
            module_feedback = {}
            for feedback in all_feedback:
                if feedback.module_id:
                    if feedback.module_id not in module_feedback:
                        module_feedback[feedback.module_id] = []
                    module_feedback[feedback.module_id].append(feedback)
            
            module_analytics = {}
            for module_id, feedbacks in module_feedback.items():
                module = Module.get_by_id(module_id)
                if module:
                    module_analytics[module.name] = {
                        'total_feedback': len(feedbacks),
                        'average_rating': sum(f.rating for f in feedbacks) / len(feedbacks),
                        'rating_distribution': FeedbackSurvey.get_rating_distribution(module_id)
                    }
            
            # Difficulty level analysis
            difficulty_distribution = defaultdict(int)
            for feedback in all_feedback:
                if feedback.difficulty_level:
                    difficulty_distribution[feedback.difficulty_level] += 1
            
            return {
                'overall': {
                    'total_feedback': total_feedback,
                    'average_rating': round(average_rating, 2),
                    'rating_distribution': rating_distribution
                },
                'module_feedback': module_analytics,
                'difficulty_distribution': dict(difficulty_distribution)
            }
            
        except Exception as e:
            print(f"Error getting feedback analytics: {e}")
            return {}
    
    @staticmethod
    def generate_analytics_report() -> Dict[str, Any]:
        """Generate a comprehensive analytics report"""
        try:
            return {
                'system_overview': AnalyticsService.get_system_overview(),
                'user_performance': AnalyticsService.get_user_performance_analytics(),
                'module_analytics': AnalyticsService.get_module_analytics(),
                'trend_analytics': AnalyticsService.get_trend_analytics(),
                'assessment_analytics': AnalyticsService.get_assessment_analytics(),
                'simulation_analytics': AnalyticsService.get_simulation_analytics(),
                'feedback_analytics': AnalyticsService.get_feedback_analytics(),
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating analytics report: {e}")
            return {}

