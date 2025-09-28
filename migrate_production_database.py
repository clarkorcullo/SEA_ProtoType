#!/usr/bin/env python3
"""
Production Database Migration Script
Adds the highest_score column to the userprogress table in production database
"""

import os
import sys
from sqlalchemy import text, inspect
from flask import Flask

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from data_models.progress_models import UserProgress

def migrate_production_database():
    """Add highest_score column to userprogress table if it doesn't exist"""
    
    with app.app_context():
        try:
            # Check if the column already exists
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('userprogress')]
            
            if 'highest_score' in columns:
                print("✅ Column 'highest_score' already exists in userprogress table")
                return True
            
            print("🔄 Adding 'highest_score' column to userprogress table...")
            
            # Add the column with default value 0
            db.session.execute(text(
                "ALTER TABLE userprogress ADD COLUMN highest_score INTEGER DEFAULT 0"
            ))
            
            # Update existing records to set highest_score = score
            db.session.execute(text(
                "UPDATE userprogress SET highest_score = score WHERE highest_score = 0"
            ))
            
            db.session.commit()
            print("✅ Successfully added 'highest_score' column to userprogress table")
            print("✅ Updated existing records with current scores")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            return False

def verify_migration():
    """Verify that the migration was successful"""
    
    with app.app_context():
        try:
            # Check if the column exists
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('userprogress')]
            
            if 'highest_score' in columns:
                print("✅ Migration verification successful: 'highest_score' column exists")
                
                # Check if we can query the column
                result = db.session.execute(text("SELECT COUNT(*) FROM userprogress")).scalar()
                print(f"✅ Found {result} records in userprogress table")
                
                return True
            else:
                print("❌ Migration verification failed: 'highest_score' column not found")
                return False
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return False

if __name__ == "__main__":
    print("🚀 Starting Production Database Migration...")
    print("=" * 50)
    
    # Run migration
    if migrate_production_database():
        print("\n🔍 Verifying migration...")
        if verify_migration():
            print("\n🎉 Production database migration completed successfully!")
            print("✅ Your application should now work properly on Render")
        else:
            print("\n❌ Migration verification failed")
            sys.exit(1)
    else:
        print("\n❌ Migration failed")
        sys.exit(1)
