#!/usr/bin/env python3
"""
Management script for Social Engineering Awareness Program
Provides utilities for database management and application maintenance
"""

import os
import sys
import argparse
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, init_database, create_default_data
from data_models import User, Module, KnowledgeCheckQuestion
from business_services import UserService

def reset_database():
    """Reset the database and recreate all tables"""
    with app.app_context():
        print("🗑️ Dropping all tables...")
        db.drop_all()
        print("✅ Tables dropped successfully")
        
        print("🔧 Creating new tables...")
        init_database()
        print("✅ Database reset completed")

def create_admin_user(username, email, password):
    """Create a new admin user"""
    with app.app_context():
        try:
            admin_data = {
                'username': username,
                'email': email,
                'password': password,
                'full_name': 'System Administrator',
                'specialization': 'Information Technology',
                'year_level': '4th Year'
            }
            user = UserService.create_user(admin_data)
            print(f"✅ Admin user '{username}' created successfully")
            return user
        except Exception as e:
            print(f"❌ Failed to create admin user: {e}")
            return None

def list_users():
    """List all users in the system"""
    with app.app_context():
        users = User.get_all()
        if not users:
            print("📝 No users found in the system")
            return
        
        print(f"📝 Found {len(users)} users:")
        print("-" * 80)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.full_name}")
            print(f"Specialization: {user.specialization}")
            print(f"Year Level: {user.year_level}")
            print(f"Modules Completed: {user.modules_completed}")
            print(f"Total Score: {user.total_score}")
            print(f"Created: {user.created_at}")
            print("-" * 80)

def list_modules():
    """List all modules in the system"""
    with app.app_context():
        modules = Module.get_all_ordered()
        if not modules:
            print("📚 No modules found in the system")
            return
        
        print(f"📚 Found {len(modules)} modules:")
        print("-" * 80)
        for module in modules:
            print(f"ID: {module.id}")
            print(f"Order: {module.order}")
            print(f"Name: {module.name}")
            print(f"Description: {module.description[:100]}...")
            print(f"Has Simulation: {module.has_simulation}")
            print(f"Simulation Type: {module.simulation_type}")
            print(f"Question Count: {module.question_count}")
            print(f"Completion Rate: {module.completion_rate:.1f}%")
            print(f"Average Score: {module.average_score:.1f}%")
            print("-" * 80)

def backup_database():
    """Create a backup of the database"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_social_engineering_awareness_{timestamp}.db"
    
    try:
        shutil.copy2('social_engineering_awareness.db', backup_filename)
        print(f"✅ Database backed up to: {backup_filename}")
    except Exception as e:
        print(f"❌ Failed to backup database: {e}")

def show_statistics():
    """Show system statistics"""
    with app.app_context():
        total_users = User.count()
        total_modules = Module.count()
        total_questions = KnowledgeCheckQuestion.count()
        
        print("📊 System Statistics:")
        print("-" * 40)
        print(f"Total Users: {total_users}")
        print(f"Total Modules: {total_modules}")
        print(f"Total Questions: {total_questions}")
        
        if total_users > 0:
            # Get some user statistics
            users = User.get_all()
            completed_modules = sum(user.modules_completed for user in users)
            total_scores = sum(user.total_score for user in users)
            
            print(f"Total Modules Completed: {completed_modules}")
            print(f"Average Modules per User: {completed_modules / total_users:.1f}")
            print(f"Total Scores: {total_scores}")
            print(f"Average Score per User: {total_scores / total_users:.1f}")

def main():
    parser = argparse.ArgumentParser(description='Social Engineering Awareness Program Management')
    parser.add_argument('command', choices=[
        'reset-db', 'create-admin', 'list-users', 'list-modules', 
        'backup', 'stats', 'init'
    ], help='Command to execute')
    
    parser.add_argument('--username', help='Username for admin creation')
    parser.add_argument('--email', help='Email for admin creation')
    parser.add_argument('--password', help='Password for admin creation')
    
    args = parser.parse_args()
    
    if args.command == 'reset-db':
        confirm = input("⚠️ This will delete all data. Are you sure? (yes/no): ")
        if confirm.lower() == 'yes':
            reset_database()
        else:
            print("❌ Operation cancelled")
    
    elif args.command == 'create-admin':
        if not all([args.username, args.email, args.password]):
            print("❌ Please provide --username, --email, and --password")
            return
        create_admin_user(args.username, args.email, args.password)
    
    elif args.command == 'list-users':
        list_users()
    
    elif args.command == 'list-modules':
        list_modules()
    
    elif args.command == 'backup':
        backup_database()
    
    elif args.command == 'stats':
        show_statistics()
    
    elif args.command == 'init':
        with app.app_context():
            print("🔧 Initializing database...")
            init_database()
            print("✅ Database initialized successfully")

if __name__ == '__main__':
    main()
