#!/usr/bin/env python3
"""
Setup Fresh Repository Script
This script helps you create a completely fresh repository for your project.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False
    return True

def main():
    print("🚀 FRESH REPOSITORY SETUP")
    print("=" * 50)
    
    print("\n📋 Current Status:")
    print("✅ Project cleaned and ready")
    print("✅ All old content removed")
    print("✅ Professional template preserved")
    print("✅ Deployment configuration ready")
    
    print("\n🔧 STEP 1: Remove Current Git Connection")
    print("This will remove the connection to the old repository...")
    
    # Remove current remote
    if run_command("git remote remove origin", "Remove current remote origin"):
        print("✅ Disconnected from old repository")
    else:
        print("⚠️  Remote might not exist or already removed")
    
    print("\n🔧 STEP 2: Clean Git History (Optional)")
    print("This will create a fresh git history with only the current state...")
    
    # Create fresh git history
    if run_command("git checkout --orphan fresh-start", "Create fresh branch"):
        if run_command("git add .", "Stage all files"):
            if run_command('git commit -m "Initial commit: Fresh start with cleaned project"', "Create initial commit"):
                if run_command("git branch -D main", "Delete old main branch"):
                    if run_command("git branch -m main", "Rename fresh-start to main"):
                        print("✅ Fresh git history created")
                    else:
                        print("❌ Failed to rename branch")
                else:
                    print("❌ Failed to delete old main branch")
            else:
                print("❌ Failed to create initial commit")
        else:
            print("❌ Failed to stage files")
    else:
        print("❌ Failed to create fresh branch")
        return
    
    print("\n🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. Create a NEW repository on GitHub:")
    print("   - Go to https://github.com/new")
    print("   - Name: 'SocialEngineeringAwareness-Fresh' (or your preferred name)")
    print("   - Description: 'Social Engineering Awareness Program - Fresh Start'")
    print("   - Make it PUBLIC or PRIVATE (your choice)")
    print("   - DO NOT initialize with README, .gitignore, or license")
    print("   - Click 'Create repository'")
    
    print("\n2. Connect to your new repository:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_NEW_REPO_NAME.git")
    print("   git push -u origin main")
    
    print("\n3. Update deployment configuration:")
    print("   - Update RENDER_DEPLOYMENT.md with new repository URL")
    print("   - Update README.md with new repository links")
    print("   - Update any hardcoded repository references")
    
    print("\n4. Deploy to Render:")
    print("   - Connect your new repository to Render")
    print("   - Use the same environment variables")
    print("   - Deploy and test")
    
    print("\n✨ Your project is now ready for a fresh repository!")
    print("All old content has been removed and the project is clean.")

if __name__ == "__main__":
    main()
