"""
Module service for handling module-related business logic
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from data_models.content_models import Module, KnowledgeCheckQuestion
from data_models.progress_models import UserProgress, ProgressStatus
from data_models.user_models import User

class ModuleService:
    """Service class for module operations"""
    
    def __init__(self):
        """Initialize module service"""
        pass
    
    @staticmethod
    def get_user_progress_for_modules(user_id: int) -> Dict[int, Dict[str, Any]]:
        """Get user progress for all modules"""
        try:
            modules = Module.get_all_ordered()
            progress_data = {}
            
            for module in modules:
                progress = UserProgress.get_module_progress(user_id, module.id)
                if progress:
                    progress_data[module.id] = {
                        'status': progress.status,
                        'score': progress.score,
                        'attempts': progress.attempts,
                        'time_spent': progress.time_spent,
                        'completed_at': progress.completed_at,
                        'is_completed': progress.is_completed
                    }
                else:
                    progress_data[module.id] = {
                        'status': ProgressStatus.NOT_STARTED.value,
                        'score': 0,
                        'attempts': 0,
                        'time_spent': 0,
                        'completed_at': None,
                        'is_completed': False
                    }
            
            return progress_data
            
        except Exception as e:
            print(f"Error getting user progress for modules: {e}")
            return {}
    
    @staticmethod
    def get_module_with_progress(module_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Get module with user progress"""
        try:
            module = Module.get_by_id(module_id)
            if not module:
                return None
            
            progress = UserProgress.get_module_progress(user_id, module_id)
            
            module_data = module.get_module_statistics()
            module_data['user_progress'] = progress.to_dict() if progress else None
            module_data['question_count'] = module.question_count
            
            return module_data
            
        except Exception as e:
            print(f"Error getting module with progress: {e}")
            return None
    
    @staticmethod
    def start_module(user_id: int, module_id: int) -> bool:
        """Start a module for a user"""
        try:
            progress = UserProgress.get_module_progress(user_id, module_id)
            if not progress:
                progress = UserProgress(
                    user_id=user_id,
                    module_id=module_id,
                    status=ProgressStatus.IN_PROGRESS.value
                )
                progress.save()
            else:
                progress.start_progress()
            
            return True
            
        except Exception as e:
            print(f"Error starting module: {e}")
            return False
    
    @staticmethod
    def complete_module(user_id: int, module_id: int, score: int) -> bool:
        """Complete a module for a user"""
        try:
            progress = UserProgress.get_module_progress(user_id, module_id)
            if not progress:
                progress = UserProgress(
                    user_id=user_id,
                    module_id=module_id
                )
            
            success = progress.complete_progress(score)
            if success:
                # Update user's overall progress
                user = User.get_by_id(user_id)
                if user:
                    user.update_progress(module_id, score)
            
            return success
            
        except Exception as e:
            print(f"Error completing module: {e}")
            return False
    
    @staticmethod
    def get_next_available_module(user_id: int) -> Optional[Module]:
        """Get the next available module for a user"""
        try:
            completed_modules = UserProgress.get_completed_modules(user_id)
            completed_module_ids = {p.module_id for p in completed_modules}
            
            all_modules = Module.get_all_ordered()
            
            for module in all_modules:
                if module.id not in completed_module_ids:
                    return module
            
            return None
            
        except Exception as e:
            print(f"Error getting next available module: {e}")
            return None
    
    @staticmethod
    def get_module_prerequisites(module_id: int) -> List[Module]:
        """Get prerequisite modules for a given module"""
        try:
            current_module = Module.get_by_id(module_id)
            if not current_module:
                return []
            
            # Get all modules with order less than current module
            prerequisites = Module.query.filter(
                Module.order < current_module.order
            ).order_by(Module.order).all()
            
            return prerequisites
            
        except Exception as e:
            print(f"Error getting module prerequisites: {e}")
            return []
    
    @staticmethod
    def check_module_eligibility(user_id: int, module_id: int) -> Dict[str, Any]:
        """Check if user is eligible to access a module"""
        try:
            module = Module.get_by_id(module_id)
            if not module:
                return {'eligible': False, 'reason': 'Module not found'}
            
            # Get prerequisites
            prerequisites = ModuleService.get_module_prerequisites(module_id)
            
            # Check if all prerequisites are completed
            for prereq in prerequisites:
                progress = UserProgress.get_module_progress(user_id, prereq.id)
                if not progress or not progress.is_completed:
                    return {
                        'eligible': False,
                        'reason': f'Must complete {prereq.name} first',
                        'prerequisite': prereq
                    }
            
            return {'eligible': True, 'reason': 'All prerequisites completed'}
            
        except Exception as e:
            print(f"Error checking module eligibility: {e}")
            return {'eligible': False, 'reason': 'Error checking eligibility'}
    
    @staticmethod
    def get_module_statistics(module_id: int) -> Dict[str, Any]:
        """Get comprehensive statistics for a module"""
        try:
            module = Module.get_by_id(module_id)
            if not module:
                return {}
            
            # Get basic module statistics
            stats = module.get_module_statistics()
            
            # Get user progress statistics
            all_progress = UserProgress.query.filter_by(module_id=module_id).all()
            
            if all_progress:
                total_users = len(set(p.user_id for p in all_progress))
                completed_users = len([p for p in all_progress if p.is_completed])
                average_score = sum(p.score for p in all_progress if p.is_completed) / completed_users if completed_users > 0 else 0
                average_time = sum(p.time_spent for p in all_progress if p.is_completed) / completed_users if completed_users > 0 else 0
                
                stats.update({
                    'total_users': total_users,
                    'completed_users': completed_users,
                    'completion_rate': (completed_users / total_users) * 100 if total_users > 0 else 0,
                    'average_score': round(average_score, 2),
                    'average_time_minutes': round(average_time, 2)
                })
            
            return stats
            
        except Exception as e:
            print(f"Error getting module statistics: {e}")
            return {}
    
    @staticmethod
    def get_user_learning_path(user_id: int) -> List[Dict[str, Any]]:
        """Get user's learning path with progress"""
        try:
            modules = Module.get_all_ordered()
            learning_path = []
            
            for module in modules:
                progress = UserProgress.get_module_progress(user_id, module.id)
                eligibility = ModuleService.check_module_eligibility(user_id, module.id)
                
                module_info = {
                    'module': module.to_dict(),
                    'progress': progress.to_dict() if progress else None,
                    'eligible': eligibility['eligible'],
                    'reason': eligibility['reason'],
                    'question_count': module.question_count,
                    'has_simulation': module.has_simulation
                }
                
                learning_path.append(module_info)
            
            return learning_path
            
        except Exception as e:
            print(f"Error getting user learning path: {e}")
            return []
    
    @staticmethod
    def update_module_content(module_id: int, content_data: Dict[str, Any]) -> bool:
        """Update module content"""
        try:
            module = Module.get_by_id(module_id)
            if not module:
                return False
            
            # Validate content data
            allowed_fields = ['name', 'description', 'content', 'has_simulation', 'simulation_type']
            update_data = {k: v for k, v in content_data.items() if k in allowed_fields}
            
            return module.update(**update_data)
            
        except Exception as e:
            print(f"Error updating module content: {e}")
            return False
    
    @staticmethod
    def get_modules_by_simulation_type(simulation_type: str) -> List[Module]:
        """Get modules by simulation type"""
        try:
            return Module.query.filter_by(
                has_simulation=True,
                simulation_type=simulation_type
            ).order_by(Module.order).all()
            
        except Exception as e:
            print(f"Error getting modules by simulation type: {e}")
            return []

