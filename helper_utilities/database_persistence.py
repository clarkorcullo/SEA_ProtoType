"""
Database Persistence Utilities
Handles database backup, restore, and persistence for deployment environments
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabasePersistence:
    """Handles database persistence and backup operations"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            self.db_path = db_uri.replace('sqlite:///', '')
        elif db_uri.startswith('sqlite:////'):
            self.db_path = db_uri.replace('sqlite:////', '/')
        else:
            # For PostgreSQL or other databases, we can't use direct file access
            self.db_path = None
    
    def backup_database(self) -> Dict[str, Any]:
        """Create a backup of the current database"""
        try:
            if not os.path.exists(self.db_path):
                return {'success': False, 'error': 'Database file not found'}
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"{self.db_path}.backup_{timestamp}"
            
            # Copy database file
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"Database backup created: {backup_path}")
            return {
                'success': True, 
                'backup_path': backup_path,
                'timestamp': timestamp
            }
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def restore_database(self, backup_path: str) -> Dict[str, Any]:
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                return {'success': False, 'error': 'Backup file not found'}
            
            # Create backup of current database before restore
            current_backup = self.backup_database()
            
            # Restore from backup
            import shutil
            shutil.copy2(backup_path, self.db_path)
            
            logger.info(f"Database restored from: {backup_path}")
            return {
                'success': True,
                'restored_from': backup_path,
                'current_backup': current_backup.get('backup_path')
            }
            
        except Exception as e:
            logger.error(f"Database restore failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def export_user_data(self) -> Dict[str, Any]:
        """Export user data to JSON format"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Export users
            users = []
            cursor.execute("SELECT * FROM user")
            for row in cursor.fetchall():
                users.append(dict(row))
            
            # Export user progress
            progress = []
            cursor.execute("SELECT * FROM user_progress")
            for row in cursor.fetchall():
                progress.append(dict(row))
            
            # Export assessment results
            assessments = []
            cursor.execute("SELECT * FROM assessment_result")
            for row in cursor.fetchall():
                assessments.append(dict(row))
            
            conn.close()
            
            export_data = {
                'users': users,
                'user_progress': progress,
                'assessment_results': assessments,
                'export_timestamp': datetime.now().isoformat(),
                'total_users': len(users),
                'total_progress_records': len(progress),
                'total_assessments': len(assessments)
            }
            
            logger.info(f"User data exported: {len(users)} users, {len(progress)} progress records, {len(assessments)} assessments")
            return {'success': True, 'data': export_data}
            
        except Exception as e:
            logger.error(f"User data export failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def import_user_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Import user data from JSON format"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            imported_count = 0
            
            # Import users
            if 'users' in data:
                for user_data in data['users']:
                    try:
                        # Insert user (handle duplicates)
                        cursor.execute("""
                            INSERT OR REPLACE INTO user 
                            (id, username, email, password_hash, full_name, specialization, 
                             year_level, birthday, address, profile_picture, modules_completed, 
                             total_score, simulations_completed, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            user_data.get('id'),
                            user_data.get('username'),
                            user_data.get('email'),
                            user_data.get('password_hash'),
                            user_data.get('full_name'),
                            user_data.get('specialization'),
                            user_data.get('year_level'),
                            user_data.get('birthday'),
                            user_data.get('address'),
                            user_data.get('profile_picture'),
                            user_data.get('modules_completed', 0),
                            user_data.get('total_score', 0),
                            user_data.get('simulations_completed', 0),
                            user_data.get('created_at'),
                            user_data.get('updated_at')
                        ))
                        imported_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to import user {user_data.get('username')}: {e}")
            
            conn.commit()
            conn.close()
            
            logger.info(f"User data imported: {imported_count} users")
            return {'success': True, 'imported_count': imported_count}
            
        except Exception as e:
            logger.error(f"User data import failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def ensure_admin_user(self, username: str = 'administrator', 
                         email: str = 'admin@mmdc.edu.ph',
                         password: str = 'Admin123!@#2025') -> Dict[str, Any]:
        """Ensure admin user exists with correct credentials"""
        try:
            # If we can't access SQLite directly (e.g., PostgreSQL), use Flask app context
            if not self.db_path:
                return self._ensure_admin_user_via_flask(username, email, password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if admin user exists
            cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
            admin_user = cursor.fetchone()
            
            if admin_user:
                # Update existing admin user
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash(password)
                
                cursor.execute("""
                    UPDATE user SET 
                        email = ?, password_hash = ?, full_name = ?, 
                        specialization = ?, year_level = ?, updated_at = ?
                    WHERE username = ?
                """, (email, password_hash, 'System Administrator', 
                      'Information Technology', '4th Year', 
                      datetime.now().isoformat(), username))
                
                logger.info(f"Admin user updated: {username}")
            else:
                # Create new admin user
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash(password)
                
                cursor.execute("""
                    INSERT INTO user 
                    (username, email, password_hash, full_name, specialization, 
                     year_level, modules_completed, total_score, simulations_completed, 
                     created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, email, password_hash, 'System Administrator',
                      'Information Technology', '4th Year', 0, 0, 0,
                      datetime.now().isoformat(), datetime.now().isoformat()))
                
                logger.info(f"Admin user created: {username}")
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'username': username, 'email': email}
            
        except Exception as e:
            logger.error(f"Failed to ensure admin user: {e}")
            return {'success': False, 'error': str(e)}
    
    def _ensure_admin_user_via_flask(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Ensure admin user using Flask app context (for PostgreSQL or when SQLite path is not accessible)"""
        try:
            from data_models.user_models import User
            from business_services.user_service import UserService
            
            with self.app.app_context():
                # Check if admin user exists
                admin_user = User.get_by_username(username)
                
                if admin_user:
                    # Update existing admin user
                    admin_user.email = email
                    admin_user.set_password(password)
                    admin_user.full_name = 'System Administrator'
                    admin_user.specialization = 'Information Technology'
                    admin_user.year_level = '4th Year'
                    admin_user.save()
                    logger.info(f"Admin user updated: {username}")
                else:
                    # Create new admin user
                    admin_data = {
                        'username': username,
                        'email': email,
                        'password': password,
                        'full_name': 'System Administrator',
                        'specialization': 'Information Technology',
                        'year_level': '4th Year'
                    }
                    UserService.create_user(admin_data)
                    logger.info(f"Admin user created: {username}")
                
                return {'success': True, 'username': username, 'email': email}
                
        except Exception as e:
            logger.error(f"Failed to ensure admin user via Flask: {e}")
            return {'success': False, 'error': str(e)}
