#!/usr/bin/env python3
"""
Database Migration Script for Social Engineering Awareness Program
Safely adds missing security columns to the User table
"""

import os
import sys
from datetime import datetime
from sqlalchemy import text, inspect

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from data_models.user_models import User

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns(table_name)]
            return column_name in columns
    except Exception as e:
        print(f"Error checking column {column_name}: {e}")
        return False

def add_column_safely(table_name, column_name, column_definition):
    """Safely add a column if it doesn't exist"""
    try:
        if not check_column_exists(table_name, column_name):
            print(f"Adding column {column_name} to {table_name}...")
            db.session.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"))
            db.session.commit()
            print(f"Successfully added {column_name}")
            return True
        else:
            print(f"Column {column_name} already exists")
            return True
    except Exception as e:
        print(f"Error adding column {column_name}: {e}")
        db.session.rollback()
        return False

def migrate_user_security_columns():
    """Add missing security columns to User table"""
    print("Starting User table security columns migration...")
    
    # Define the columns to add
    security_columns = [
        ("failed_login_attempts", "INTEGER DEFAULT 0"),
        ("account_locked_until", "DATETIME"),
        ("last_login_ip", "VARCHAR(45)"),
        ("last_login_time", "DATETIME"),
        ("password_changed_at", "DATETIME"),
        ("two_factor_enabled", "BOOLEAN DEFAULT 0"),
        ("two_factor_secret", "VARCHAR(32)")
    ]
    
    success_count = 0
    total_columns = len(security_columns)
    
    with app.app_context():
        for column_name, column_definition in security_columns:
            if add_column_safely('user', column_name, column_definition):
                success_count += 1
    
    print(f"\nMigration Summary:")
    print(f"   Successfully added: {success_count}/{total_columns} columns")
    print(f"   Failed: {total_columns - success_count}/{total_columns} columns")
    
    # Set default values for password_changed_at column
    if check_column_exists('user', 'password_changed_at'):
        print("Setting default values for password_changed_at column...")
        try:
            with app.app_context():
                db.session.execute(text("UPDATE user SET password_changed_at = created_at WHERE password_changed_at IS NULL"))
                db.session.commit()
                print("Successfully set default values for password_changed_at")
        except Exception as e:
            print(f"Warning: Could not set default values for password_changed_at: {e}")
            with app.app_context():
                db.session.rollback()
    
    return success_count == total_columns

def verify_migration():
    """Verify that all required columns exist"""
    print("\nVerifying migration...")
    
    required_columns = [
        'failed_login_attempts',
        'account_locked_until', 
        'last_login_ip',
        'last_login_time',
        'password_changed_at',
        'two_factor_enabled',
        'two_factor_secret'
    ]
    
    missing_columns = []
    
    with app.app_context():
        for column in required_columns:
            if not check_column_exists('user', column):
                missing_columns.append(column)
    
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return False
    else:
        print("All required columns exist")
        return True

def test_user_model():
    """Test that the User model works correctly"""
    print("\nTesting User model...")
    
    try:
        with app.app_context():
            # Try to query a user
            user = User.query.first()
            if user:
                print(f"User model query successful: {user.username}")
                
                # Test accessing new security attributes
                print(f"   - failed_login_attempts: {user.failed_login_attempts}")
                print(f"   - two_factor_enabled: {user.two_factor_enabled}")
                print(f"   - account_locked_until: {user.account_locked_until}")
                
                return True
            else:
                print("No users found in database")
                return True
                
    except Exception as e:
        print(f"User model test failed: {e}")
        return False

def main():
    """Main migration function"""
    print("Starting Database Migration for Security Columns")
    print("=" * 60)
    
    try:
        # Step 1: Add missing columns
        if not migrate_user_security_columns():
            print("Migration failed")
            return False
        
        # Step 2: Verify migration
        if not verify_migration():
            print("Migration verification failed")
            return False
        
        # Step 3: Test User model
        if not test_user_model():
            print("User model test failed")
            return False
        
        print("\nMigration completed successfully!")
        print("Database is now compatible with the updated User model")
        return True
        
    except Exception as e:
        print(f"Migration failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
