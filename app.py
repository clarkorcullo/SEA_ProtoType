"""
🛡️ SOCIAL ENGINEERING AWARENESS PROGRAM
========================================

Main Flask application for the Social Engineering Awareness Program.
This file contains all routes, middleware, and application configuration.

ARCHITECTURE:
- Clean Architecture with Service Layer Pattern
- Object-Oriented Programming principles
- Separation of concerns between routes and business logic
- Comprehensive error handling and logging

ORGANIZATION:
1. IMPORTS AND SETUP
2. CONFIGURATION AND INITIALIZATION
3. DATABASE INITIALIZATION
4. AUTHENTICATION ROUTES
5. LEARNING ROUTES
6. ASSESSMENT ROUTES
7. SIMULATION ROUTES
8. PROGRESS AND ANALYTICS ROUTES
9. SYSTEM ROUTES
10. ERROR HANDLERS
11. APPLICATION ENTRY POINT

Author: Capstone Project Team
Version: 1.0.0
License: MIT
"""

# =============================================================================
# 1. IMPORTS AND SETUP
# =============================================================================

# Standard library imports
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
import random
import json
import secrets

# Third-party imports
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy import text

# Local application imports
from data_models.base_models import db
from data_models import (
    User, PasswordResetToken, Module, KnowledgeCheckQuestion, 
    FinalAssessmentQuestion, UserProgress, AssessmentResult, 
    SimulationResult, FeedbackSurvey, SimpleReflection
)
# Assessment models imported only when needed to avoid circular imports
from business_services import (
    UserService, AssessmentService, SimulationService
)
# Assessment routes will be added directly to app.py
from config import config

# =============================================================================
# 2. LOGGING CONFIGURATION
# =============================================================================

def setup_logging():
    """
    Configure comprehensive logging for the application.
    
    Features:
    - Console and file output
    - UTF-8 encoding support
    - Configurable log levels
    - Structured formatting
    
    Returns:
        logging.Logger: Configured logger instance
    """
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_file = os.environ.get('LOG_FILE', 'app.log')
    
    # Create formatter that handles Unicode properly
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Timed rotating file handler: rotate at midnight, keep last 3 days
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=3,
        encoding='utf-8',
        utc=False
    )
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)

# Initialize logging
logger = setup_logging()

# =============================================================================
# 3. FLASK APPLICATION SETUP
# =============================================================================

# Create Flask application instance
app = Flask(__name__)

# Load environment-based configuration (tolerate extra whitespace and unknown keys)
env_value = os.environ.get('FLASK_ENV', 'production') or 'production'
config_name = env_value.strip()
if config_name not in config:
    # Fallback to production if an unknown value (e.g., trailing spaces) is provided
    config_name = 'production'
app.config.from_object(config[config_name])

# Configure reverse proxy for production deployment (Render/Heroku)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure URL building for production
if os.environ.get('RENDER'):
    app.config['SERVER_NAME'] = None  # Allow URL building without server name
    app.config['PREFERRED_URL_SCHEME'] = 'https'

# =============================================================================
# 4. EXTENSIONS AND SERVICES INITIALIZATION
# =============================================================================

# Initialize database
db.init_app(app)

# Ensure schema compatibility at startup (handles Postgres deployments)
with app.app_context():
    try:
        # Create tables if not exist
        db.create_all()
        # Try to widen password_hash column if it's too small (Postgres only)
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if inspector.has_table('user'):
            # Only run on Postgres (SQLite len is flexible for TEXT)
            if db.engine.url.get_backend_name() in ['postgresql', 'postgres']:
                try:
                    db.session.execute(text(
                        "ALTER TABLE \"user\" ALTER COLUMN password_hash TYPE VARCHAR(255)"
                    ))
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        # Auto-migrate highest_score column for production deployments
        try:
            if inspector.has_table('userprogress'):
                columns = [col['name'] for col in inspector.get_columns('userprogress')]
                if 'highest_score' not in columns:
                    logger.info("[MIGRATION] Adding highest_score column to userprogress table...")
                    db.session.execute(text(
                        "ALTER TABLE userprogress ADD COLUMN highest_score INTEGER DEFAULT 0"
                    ))
                    # Update existing records to set highest_score = score
                    db.session.execute(text(
                        "UPDATE userprogress SET highest_score = score WHERE highest_score = 0"
                    ))
                    db.session.commit()
                    logger.info("[MIGRATION] Successfully added highest_score column")
        except Exception as e:
            logger.warning(f"[MIGRATION] Could not migrate highest_score column: {e}")
            db.session.rollback()

        # Ensure modules have drawer placeholders so UI renders consistently in production
        try:
            def build_standard_skeleton(module_index: int) -> str:
                # Generic three-section skeleton per module
                return (
                    f'<div class="drawer-subcontent" id="content-sub{module_index}-1"><div class="content-wrapper" id="placeholder-sub{module_index}-1"></div></div>'
                    f'<div class="drawer-subcontent" id="content-sub{module_index}-2"><div class="content-wrapper"></div></div>'
                    f'<div class="drawer-subcontent" id="content-sub{module_index}-3"><div class="content-wrapper"></div></div>'
                )

            modules = Module.get_all_ordered()
            for mod in modules:
                # Use different index base per module to avoid ID collisions across lessons
                index_base = mod.order if mod.order and mod.order > 0 else 1
                needs_standardization = not mod.content or 'drawer-subcontent' not in mod.content
                if needs_standardization:
                    standardized = build_standard_skeleton(index_base)
                    mod.content = (standardized + (mod.content or ''))
                    mod.save()
        except Exception:
            pass
        # Import content seed on Render to mirror local content
        try:
            if os.environ.get('RENDER'):
                seed_path = os.path.join(os.path.dirname(__file__), 'content_seed', 'modules.json')
                if os.path.exists(seed_path):
                    import json
                    from data_models.content_models import Module, KnowledgeCheckQuestion
                    with open(seed_path, 'r', encoding='utf-8') as f:
                        payload = json.load(f)
                    for m in payload.get('modules', []):
                        existing = Module.get_by_order(m.get('order'))
                        if existing:
                            existing.name = m.get('name', existing.name)
                            existing.description = m.get('description', existing.description)
                            existing.content = m.get('content', existing.content)
                            existing.has_simulation = m.get('has_simulation', existing.has_simulation)
                            existing.simulation_type = m.get('simulation_type', existing.simulation_type)
                            existing.save()
                        else:
                            created = Module(
                                name=m.get('name', ''),
                                description=m.get('description', ''),
                                content=m.get('content', ''),
                                order=m.get('order'),
                                has_simulation=m.get('has_simulation', False),
                                simulation_type=m.get('simulation_type')
                            )
                            created.save()
                            existing = created
                        # Replace questions for set=1
                        if existing:
                            qs = KnowledgeCheckQuestion.get_by_module_and_set(existing.id, 1)
                            for q in qs:
                                db.session.delete(q)
                            db.session.commit()
                            for q in m.get('questions', []):
                                nq = KnowledgeCheckQuestion(
                                    question_text=q['question_text'],
                                    option_a=q['option_a'],
                                    option_b=q['option_b'],
                                    option_c=q['option_c'],
                                    option_d=q['option_d'],
                                    correct_answer=q['correct_answer'],
                                    explanation=q['explanation'],
                                    question_set=q.get('question_set', 1),
                                    module_id=existing.id
                                )
                                nq.save()
                    # Replace final assessment questions as well
                    from data_models.content_models import FinalAssessmentQuestion
                    fa_existing = FinalAssessmentQuestion.query.all()
                    for q in fa_existing:
                        db.session.delete(q)
                    db.session.commit()
                    for q in payload.get('final_assessment_questions', []):
                        nq = FinalAssessmentQuestion(
                            question_text=q['question_text'],
                            option_a=q['option_a'],
                            option_b=q['option_b'],
                            option_c=q['option_c'],
                            option_d=q['option_d'],
                            correct_answer=q['correct_answer'],
                            explanation=q['explanation'],
                            question_set=q.get('question_set', 1)
                        )
                        nq.save()
        except Exception:
            pass
    except Exception:
        pass

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize business services
user_service = UserService()
assessment_service = AssessmentService()
simulation_service = SimulationService()

# =============================================================================
# 5. DATABASE INITIALIZATION FUNCTIONS
# =============================================================================

def init_database():
    """
    Initialize database with all models and create default data.
    
    This function:
    - Creates all database tables
    - Populates default educational content
    - Creates admin user if not exists
    - Sets up initial modules and questions
    
    Raises:
        Exception: If database initialization fails
    """
    try:
        db.create_all()
        create_default_data()
        logger.info("[SUCCESS] Database initialized successfully")
    except Exception as e:
        logger.error(f"[ERROR] Database initialization error: {e}")
        raise

def create_default_data():
    """
    Create default application data including admin user, modules, and questions.
    
    This function ensures the application has:
    - Default administrator account
    - All educational modules
    - Assessment questions
    - Initial configuration
    
    The function is idempotent - it won't create duplicates if data already exists.
    """
    try:
        # =====================================================================
        # ADMIN USER CREATION
        # =====================================================================
        admin_user = User.get_by_username('administrator')
        if not admin_user:
            try:
                admin_data = {
                    'username': app.config.get('DEFAULT_ADMIN_USERNAME', 'administrator'),
                    'email': app.config.get('DEFAULT_ADMIN_EMAIL', 'admin@mmdc.edu.ph'),
                    'password': app.config.get('DEFAULT_ADMIN_PASSWORD', 'Admin123!@#2025'),
                    'full_name': 'System Administrator',
                    'specialization': 'Information Technology',
                    'year_level': '4th Year'
                }
                user_service.create_user(admin_data)
                logger.info("[SUCCESS] Admin user created (administrator)")
            except ValueError as ve:
                if "already exists" in str(ve):
                    logger.info("[SUCCESS] Admin user already exists (administrator)")
                else:
                    logger.warning(f"[WARNING] Admin user creation issue: {ve}")
        else:
            logger.info("[SUCCESS] Admin user already exists (administrator)")

        # Ensure admin user has correct credentials (always update on startup)
        if admin_user:
            try:
                # Update admin credentials to ensure they're correct
                admin_user.email = app.config.get('DEFAULT_ADMIN_EMAIL', 'admin@mmdc.edu.ph')
                admin_user.full_name = 'System Administrator'
                admin_user.specialization = 'Information Technology'
                admin_user.year_level = '4th Year'
                
                # Set password from environment or default
                desired_pw = os.environ.get('ADMIN_PASSWORD', app.config.get('DEFAULT_ADMIN_PASSWORD', 'Admin123!@#2025'))
                admin_user.set_password(desired_pw)
                admin_user.save()
                logger.info("[SUCCESS] Admin user credentials updated (administrator)")
            except Exception as pw_e:
                logger.warning(f"[WARNING] Could not update admin credentials: {pw_e}")
        
        # =====================================================================
        # EDUCATIONAL MODULES CREATION
        # =====================================================================
        if Module.count() == 0:
            create_default_modules()
            logger.info("[SUCCESS] Default modules created")
        else:
            logger.info("[SUCCESS] Modules already exist")
        
        # =====================================================================
        # ASSESSMENT QUESTIONS CREATION
        # =====================================================================
        if KnowledgeCheckQuestion.count() == 0:
            create_default_questions()
            logger.info("[SUCCESS] Default questions created")
        else:
            logger.info("[SUCCESS] Questions already exist")
            
    except Exception as e:
        logger.error(f"[ERROR] Error creating default data: {e}")
        raise

# =============================================================================
# 6. FLASK-LOGIN USER LOADER
# =============================================================================

@login_manager.user_loader
def load_user(user_id):
    """
    Load user for Flask-Login authentication.
    
    Args:
        user_id (str): User ID from session
        
    Returns:
        User: User object if found, None otherwise
    """
    try:
        return User.get_by_id(int(user_id))
    except Exception as e:
        logger.error(f"Error loading user {user_id}: {e}")
        return None

# =============================================================================
# 7. EDUCATIONAL CONTENT CREATION FUNCTIONS
# =============================================================================

def create_default_modules():
    """
    Create default learning modules with content from modules folder.
    
    This function:
    - Imports content from learning_modules/
    - Creates Module objects in database
    - Sets up simulation types for applicable modules
    - Handles fallback content if imports fail
    """
    try:
        # Import module content classes - TEMPORARILY DISABLED
        # from learning_modules import (
        #     Module1Content, Module2Content, Module3Content, Module4Content,
        #     Module5Content, FinalAssessmentContent
        # )
        
        # Module content classes - TEMPORARILY DISABLED
        module_classes = []
        
        for i, module_class in enumerate(module_classes, 1):
            # Get content from module class
            content_data = module_class.get_content()
            
            # Create module data
            module_data = {
                'name': content_data['title'],
                'description': content_data['description'],
                'content': content_data['content'],
                'order': i,
                'has_simulation': i in [2, 3, 4, 5],  # Modules 2-5 have simulations
                'simulation_type': 'phishing' if i == 2 else 'pretexting' if i == 3 else 'baiting' if i == 4 else 'quid_pro_quo' if i == 5 else None
            }
            
            # Create and save module
            module = Module(**module_data)
            if module.save():
                logger.info(f"[SUCCESS] Created module {i}: {content_data['title']}")
            else:
                logger.warning(f"[ERROR] Failed to create module {i}")
                
    except Exception as e:
        logger.error(f"[ERROR] Error creating modules: {e}")
        # Fallback to basic modules if import fails
        create_fallback_modules()

def create_fallback_modules():
    """
    Create basic modules as fallback if content imports fail.
    
    This ensures the application always has some content available,
    even if the learning_modules package has issues.
    """
    modules_data = [
        {
            'name': 'What is Social Engineering',
            'description': 'Understanding the basics of social engineering attacks and human psychology',
            'content': 'Social engineering is a manipulation technique that exploits human error to gain private information...',
            'order': 1,
            'has_simulation': False
        },
        {
            'name': 'Phishing: The Digital Net',
            'description': 'Recognize, detect, and defend against phishing across email, SMS, and calls',
            'content': 'Phishing is a type of social engineering that impersonates trusted entities to steal information...',
            'order': 2,
            'has_simulation': True,
            'simulation_type': 'phishing'
        },
        {
            'name': 'Fortifying Your Accounts',
            'description': 'Understanding password security and authentication methods',
            'content': 'Password security involves creating strong passwords and using multi-factor authentication...',
            'order': 3,
            'has_simulation': True,
            'simulation_type': 'pretexting'
        },
        {
            'name': 'Immediate Action After a Suspected Attack',
            'description': 'Learn immediate response steps when you suspect a social engineering attack',
            'content': 'When you suspect a social engineering attack, immediate action is crucial to minimize damage...',
            'order': 4,
            'has_simulation': True,
            'simulation_type': 'baiting'
        },
        {
            'name': 'The Evolving Threat Landscape',
            'description': 'Understanding emerging social engineering threats and future trends',
            'content': 'Social engineering threats continue to evolve with technology and social changes...',
            'order': 5,
            'has_simulation': False
        },
        {
            'name': 'Final Assessment',
            'description': 'Comprehensive assessment covering all aspects of social engineering awareness and prevention',
            'content': 'This final assessment will test your comprehensive understanding of social engineering awareness...',
            'order': 6,
            'has_simulation': False
        }
    ]
    
    for module_data in modules_data:
        module = Module(**module_data)
        if module.save():
            logger.info(f"[SUCCESS] Created fallback module: {module_data['name']}")
        else:
            logger.warning(f"[ERROR] Failed to create fallback module: {module_data['name']}")

def create_default_questions():
    """
    Create default assessment questions for all modules.
    
    This function:
    - Imports question sets from learning_modules/
    - Creates KnowledgeCheckQuestion objects
    - Links questions to appropriate modules
    - Handles fallback questions if imports fail
    """
    try:
        # Import question classes - TEMPORARILY DISABLED
        # from learning_modules import (
        #     Module1Questions, Module2Questions, Module3Questions, Module4Questions,
        #     Module5Questions, FinalAssessmentQuestions
        # )
        
        # Question classes mapping - TEMPORARILY DISABLED
        question_classes = []
        
        for module_id, question_class in enumerate(question_classes, 1):
            # Get questions from module class
            questions_data = question_class.get_question_set_1()
            
            for question_data in questions_data:
                # Add module_id to question data
                question_data['module_id'] = module_id
                
                # Remove any fields that are not in the KnowledgeCheckQuestion model
                if 'module_source' in question_data:
                    del question_data['module_source']
                
                # Create and save question
                question = KnowledgeCheckQuestion(**question_data)
                if question.save():
                    logger.info(f"[SUCCESS] Created question for module {module_id}")
                else:
                    logger.warning(f"[ERROR] Failed to create question for module {module_id}")
                    
    except Exception as e:
        logger.error(f"[ERROR] Error creating questions: {e}")
        create_fallback_questions()

def create_fallback_questions():
    """
    Create basic questions as fallback if content imports fail.
    
    Ensures the application always has assessment questions available.
    """
    fallback_questions = [
        {
            'question_text': 'What is social engineering?',
                'option_a': 'A type of software',
                'option_b': 'A manipulation technique that exploits human error',
                'option_c': 'A hardware component',
                'option_d': 'A programming language',
                'correct_answer': 'b',
                'explanation': 'Social engineering is a manipulation technique that exploits human error to gain private information.',
            'module_id': 1
        },
        {
            'question_text': 'Which of the following is a common social engineering attack?',
            'option_a': 'Phishing',
            'option_b': 'Firewall',
            'option_c': 'Antivirus',
            'option_d': 'Encryption',
            'correct_answer': 'a',
            'explanation': 'Phishing is one of the most common social engineering attacks.',
            'module_id': 2
        }
    ]
    
    for question_data in fallback_questions:
        question = KnowledgeCheckQuestion(**question_data)
        if question.save():
            title = question_data.get('question_text', '')
            logger.info(f"[SUCCESS] Created fallback question: {title[:50]}...")
        else:
            logger.warning(f"[ERROR] Failed to create fallback question")

def seed_module1_kc_default() -> int:
    """Seed Module 1 Knowledge Check with a curated default set if none exist.

    Returns number of questions inserted.
    """
    try:
        from data_models.content_models import KnowledgeCheckQuestion
        questions = [
            {
                'question_text': 'According to Lesson 1.1, which of the following is the most accurate definition of social engineering?',
                'option_a': 'The use of complex code to bypass a digital firewall.',
                'option_b': 'The practice of analyzing social media to improve network security.',
                'option_c': 'The art of manipulating people into giving up confidential information by exploiting psychological tricks.',
                'option_d': 'The process of building better, more secure computer hardware.',
                'correct_answer': 'c',
                'explanation': "Social engineering is 'human hacking' — manipulating people using psychological tricks."
            },
            {
                'question_text': 'What is the primary way social engineering differs from a traditional technical hack?',
                'option_a': 'Social engineering is only used for pranks, while technical hacking is for serious crimes.',
                'option_b': 'Social engineering targets the human user to bypass security, while technical hacking targets vulnerabilities in software or systems.',
                'option_c': 'Social engineering requires advanced programming skills, while technical hacking does not.',
                'option_d': 'Social engineering can only be done over the phone, not through email.',
                'correct_answer': 'b',
                'explanation': 'Key difference: people vs. systems. Social engineering targets human behavior to bypass controls.'
            },
            {
                'question_text': "You receive an email 'URGENT: Your Student Portal Password Will Expire in 24 Hours!' from the 'Registrar's Office' with a link. This attack primarily uses which two principles?",
                'option_a': 'Liking and Social Proof',
                'option_b': 'Scarcity and Liking',
                'option_c': 'Authority and Urgency',
                'option_d': 'Scarcity and Authority',
                'correct_answer': 'c',
                'explanation': 'Impersonating a trusted department (Authority) and forcing quick action (Urgency).'
            },
            {
                'question_text': 'Based on the examples in the lessons (Bitcoin scam, GCash requests), what is a common motivation for social engineers?',
                'option_a': "To test a company's firewall for weaknesses.",
                'option_b': 'To make new friends and connections online.',
                'option_c': 'To gain access to information or resources for personal or financial benefit.',
                'option_d': 'To help users become more skeptical and informed.',
                'correct_answer': 'c',
                'explanation': 'Attackers aim for valuable gain: money, access, or sensitive data.'
            },
            {
                'question_text': 'A pop-up says: "FREE 1000 GEMS! Limited to the first 500 players!" This tactic relies on the principle of:',
                'option_a': 'Authority',
                'option_b': 'Liking',
                'option_c': 'Scarcity',
                'option_d': 'Social Proof',
                'correct_answer': 'c',
                'explanation': 'Creating fear of missing out (limited slots) is classic Scarcity.'
            }
        ]
        # Ensure clean slate
        KnowledgeCheckQuestion.query.filter_by(module_id=1).delete()
        db.session.commit()
        # Insert to set 1 by default
        for q in questions:
            row = KnowledgeCheckQuestion(
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                module_id=1,
                question_set=1
            )
            db.session.add(row)
        db.session.commit()
        return len(questions)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Default Module 1 KC seeding failed: {e}")
        return 0

def seed_module3_kc_default() -> int:
    """Seed Module 3 Knowledge Check with curated questions if none exist.

    Returns number of questions inserted.
    """
    try:
        from data_models.content_models import KnowledgeCheckQuestion
        # Ensure clean slate for module 3
        KnowledgeCheckQuestion.query.filter_by(module_id=3).delete()
        db.session.commit()

        questions = [
            {
                'question_text': 'According to the lesson, what is the recommended minimum length for creating a strong, secure password?',
                'option_a': '8 characters',
                'option_b': '10 characters',
                'option_c': '12 characters',
                'option_d': '16 characters',
                'correct_answer': 'c',
                'explanation': 'Correct! Lesson 3.1 recommends at least 12 characters; 14+ is even better.'
            },
            {
                'question_text': 'What is the primary purpose of Multi-Factor Authentication (MFA)?',
                'option_a': 'To automatically create strong passwords for you.',
                'option_b': 'To add a second layer of security, like a code from your phone, even if the password is known.',
                'option_c': 'To scan your emails for phishing attempts.',
                'option_d': 'To hide your personal information on social media.',
                'correct_answer': 'b',
                'explanation': "MFA is your 'double lock'—it adds a second verification step to block unauthorized access."
            },
            {
                'question_text': 'The lesson describes a "digital footprint" as:',
                'option_a': 'The antivirus software installed on your computer.',
                'option_b': 'The trail of data you leave behind from online activities (posts, likes, comments).',
                'option_c': 'A list of all your saved passwords in a password manager.',
                'option_d': 'The physical location from which you access the internet.',
                'correct_answer': 'b',
                'explanation': 'Your digital footprint is the data trail left by your online activities.'
            },
            {
                'question_text': 'The "Verification Toolkit" recommends hovering your mouse over a link before clicking to:',
                'option_a': 'Make the link load faster when clicked.',
                'option_b': 'Preview the actual destination URL to check if it is safe.',
                'option_c': 'Automatically copy the link to your clipboard.',
                'option_d': 'Report the link to IT.',
                'correct_answer': 'b',
                'explanation': 'Hovering reveals the true destination so you can spot suspicious or fake URLs safely.'
            },
            {
                'question_text': 'Why is reusing the same password for multiple accounts a major security risk?',
                'option_a': 'It can slow down your device when logging in.',
                'option_b': 'Websites will block reused passwords.',
                'option_c': 'If one site is breached, attackers can access your other accounts with the same password.',
                'option_d': 'It makes it harder to remember which password to use.',
                'correct_answer': 'c',
                'explanation': 'Password reuse means a single breach can compromise many of your accounts.'
            },
            {
                'question_text': 'Constantly posting your real-time location on social media significantly increases your risk of:',
                'option_a': 'Your account being suspended for spam.',
                'option_b': 'Cyberstalking and threats to your physical safety.',
                'option_c': 'Your password being guessed more easily.',
                'option_d': 'Your device getting a computer virus.',
                'correct_answer': 'b',
                'explanation': 'Real-time location tagging can enable cyberstalkers to track movements.'
            },
            {
                'question_text': 'You receive an email from “MyCamu Admin,” but the sender is support@mycamu-login-portal.com. The biggest red flag is:',
                'option_a': 'The display name is too simple.',
                'option_b': 'The email domain is not the official one and is designed to look similar.',
                'option_c': 'It was sent outside business hours.',
                'option_d': 'The email contains no images.',
                'correct_answer': 'b',
                'explanation': 'A mismatched or fake domain is a primary phishing indicator.'
            },
            {
                'question_text': 'According to the lesson’s privacy guidance, what is the safest initial setting for a new social media profile?',
                'option_a': 'Public',
                'option_b': 'Private',
                'option_c': 'Friends of Friends',
                'option_d': 'Customized for verified accounts only',
                'correct_answer': 'b',
                'explanation': 'Setting profiles to Private gives control over who sees your information.'
            },
            {
                'question_text': 'What is the main benefit of using a password manager like Google Password Manager or iCloud Keychain?',
                'option_a': 'Use the same simple password for everything.',
                'option_b': 'Securely create and remember long, complex, unique passwords with one master password.',
                'option_c': 'Receive alerts for every data breach on the internet.',
                'option_d': 'Delete your digital footprint online.',
                'correct_answer': 'b',
                'explanation': 'Password managers generate and store unique, strong passwords for all accounts.'
            },
            {
                'question_text': 'A text message claiming to be from GCash says your account will be locked unless you “verify” via a link. Safest action?',
                'option_a': 'Click the link immediately to prevent lockout.',
                'option_b': 'Reply and ask for more details.',
                'option_c': 'Ignore the message and verify via the official GCash app or website.',
                'option_d': 'Forward to a friend to check if it is real.',
                'correct_answer': 'c',
                'explanation': 'Always verify through official channels, not through the message itself.'
            }
        ]

        for q in questions:
            row = KnowledgeCheckQuestion(
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                module_id=3,
                question_set=1
            )
            db.session.add(row)
        db.session.commit()
        return len(questions)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Default Module 3 KC seeding failed: {e}")
        return 0

def seed_module4_kc_default() -> int:
    """Seed Module 4 Knowledge Check with curated questions if none exist.

    Returns number of questions inserted.
    """
    try:
        from data_models.content_models import KnowledgeCheckQuestion
        # Clear any existing Module 4 KC questions before seeding curated set
        KnowledgeCheckQuestion.query.filter_by(module_id=4).delete()
        db.session.commit()

        questions = [
            {
                'question_text': 'According to the lesson, what is the very first and most critical step you should take if you suspect you\'ve clicked a malicious link or that your device is infected?',
                'option_a': 'Immediately run an antivirus scan.',
                'option_b': 'Disconnect your device from the internet (Wi-Fi and mobile data).',
                'option_c': 'Change the password for your most important account.',
                'option_d': 'Report the incident to the IT Helpdesk.',
                'correct_answer': 'b',
                'explanation': 'Correct! The first step is always containment. Disconnecting your device stops the immediate threat, just like the lesson "I-isolate Mo Muna ang Device Mo" explains.'
            },
            {
                'question_text': 'The lesson introduces the concept of "Digital Bayanihan." What is the main idea behind this principle?',
                'option_a': 'Keeping a security incident to yourself to avoid causing panic.',
                'option_b': 'Only reporting an incident if you lose money.',
                'option_c': 'The collective effort of reporting an incident to protect the entire community, not just yourself.',
                'option_d': 'Asking friends for help to hack the scammer back.',
                'correct_answer': 'c',
                'explanation': '"Digital Bayanihan" means your report helps protect everyone in the MMDC community, reflecting the Filipino spirit of collective action.'
            },
            {
                'question_text': 'If your account is compromised and you need to reset your password, what is the safest method?',
                'option_a': 'Use the password reset link sent to you in a recent email.',
                'option_b': 'Go directly to the official website or app and use their "Forgot Password" or recovery feature.',
                'option_c': 'Call the customer service number you find in a text message.',
                'option_d': 'Ask a friend to log in for you and change the password.',
                'correct_answer': 'b',
                'explanation': 'The "Recovery Toolkit" stresses using official recovery links by going directly to the website. Links in emails or texts are often phishing attempts.'
            },
            {
                'question_text': 'You accidentally typed your password into a fake website. What is a crucial part of the immediate password change process?',
                'option_a': 'Change the password using a different, secure device if possible.',
                'option_b': 'Only change the password for that one account and no others.',
                'option_c': 'Write the new password down on a sticky note so you don\'t forget it.',
                'option_d': 'Wait 24 hours before changing the password to see if anything happens.',
                'correct_answer': 'a',
                'explanation': 'Use a clean device to ensure the attacker cannot capture your new password.'
            },
            {
                'question_text': 'You receive a phishing email targeting MMDC student portal credentials. According to the MMDC Reporting Protocol, who is the primary contact for this technical issue?',
                'option_a': 'The Faculty / Dean\'s Office',
                'option_b': 'The Opisina ng Estudyante (Student Affairs Office)',
                'option_c': 'The MMDC IT Helpdesk',
                'option_d': 'The Philippine National Police (PNP) Anti-Cybercrime Group',
                'correct_answer': 'c',
                'explanation': 'The IT Helpdesk is the designated channel for technical issues like phishing, malware, and compromised accounts.'
            },
            {
                'question_text': 'After you recover a compromised account, what is the single most effective step to fortify it against future attacks?',
                'option_a': 'Change your profile picture.',
                'option_b': 'Post a warning on your social media feed.',
                'option_c': 'Enable Multi-Factor Authentication (MFA).',
                'option_d': 'Delete all your old messages and emails.',
                'correct_answer': 'c',
                'explanation': 'Enabling MFA is the most effective security measure to lock down your account.'
            },
            {
                'question_text': 'For serious incidents involving financial loss, the module advises reporting to the PNP Anti-Cybercrime Group. What key guidance is given?',
                'option_a': 'Only report amounts larger than ₱10,000.',
                'option_b': 'File the report within 24 hours or it won\'t be accepted.',
                'option_c': 'Try contacting the scammer yourself first.',
                'option_d': 'Do this with guidance from MMDC staff (IT or Student Affairs).',
                'correct_answer': 'd',
                'explanation': 'Seek guidance from MMDC staff to follow correct legal procedures safely.'
            },
            {
                'question_text': 'After regaining access, the "Recovery Toolkit" advises reviewing recent activity and:',
                'option_a': 'Block every person who has recently sent you a message.',
                'option_b': 'Change your username and display name.',
                'option_c': 'Remove any unfamiliar third-party apps or services that have access to your account.',
                'option_d': 'Delete the account and create a new one.',
                'correct_answer': 'c',
                'explanation': 'Hackers may add third-party app access as a backdoor. Remove them.'
            },
            {
                'question_text': 'What is the primary goal of immediate containment (disconnecting your device from the internet) when responding to an attack?',
                'option_a': 'To save mobile data or battery life.',
                'option_b': 'To stop the attack from getting worse by cutting off the scammer\'s access and preventing malware from spreading.',
                'option_c': 'To reset your device\'s network settings automatically.',
                'option_d': 'To make it easier to locate the source of the attack.',
                'correct_answer': 'b',
                'explanation': 'Containment limits damage by stopping data theft and malware communication.'
            },
            {
                'question_text': 'A friend received a threatening message on school email. Which office handles harassment, threats, or cyberbullying under the MMDC Reporting Protocol?',
                'option_a': 'The MMDC IT Helpdesk',
                'option_b': 'Their specific course professor',
                'option_c': 'The Opisina ng Estudyante (Student Affairs Office)',
                'option_d': 'The campus security guards',
                'correct_answer': 'c',
                'explanation': 'Student Affairs is tasked with student welfare issues like threats and harassment.'
            }
        ]

        for q in questions:
            row = KnowledgeCheckQuestion(
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                module_id=4,
                question_set=1
            )
            db.session.add(row)
        db.session.commit()
        return len(questions)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Default Module 4 KC seeding failed: {e}")
        return 0

def seed_module5_kc_default() -> int:
    """Seed Module 5 Knowledge Check with curated questions if none exist.

    Returns number of questions inserted.
    """
    try:
        from data_models.content_models import KnowledgeCheckQuestion
        # Clear any existing Module 5 KC questions before seeding curated set
        KnowledgeCheckQuestion.query.filter_by(module_id=5).delete()
        db.session.commit()

        questions = [
            {
                'question_text': 'According to Lesson 5.1, how have AI tools like Large Language Models (LLMs) made phishing attacks more dangerous?',
                'option_a': 'AI adds viruses directly into the email text.',
                'option_b': 'AI can write perfectly crafted, personalized emails without the usual red flags like bad grammar or spelling errors.',
                'option_c': 'AI makes phishing emails blurry and hard to read.',
                'option_d': 'AI can only create phishing emails in English.',
                'correct_answer': 'b',
                'explanation': 'AI allows scammers to create flawless, personalized phishing emails, making old detection methods like spotting typos less reliable.'
            },
            {
                'question_text': 'The module discusses "deepfake" scams as a new frontier of social engineering. What is a deepfake?',
                'option_a': 'A very detailed and convincing fake social media profile.',
                'option_b': 'A type of computer virus that hides deep within a computer\'s files.',
                'option_c': 'AI-generated video or audio that convincingly mimics a real person\'s appearance or voice to trick someone.',
                'option_d': 'A phishing email that has no links or attachments.',
                'correct_answer': 'c',
                'explanation': 'A deepfake uses AI to create fake video or audio of a real person used for impersonation.'
            },
            {
                'question_text': 'The lesson introduces a new threat called "Quishing." What does this term refer to?',
                'option_a': 'A type of scam that asks you to answer a long series of personal questions.',
                'option_b': 'An attack where scammers use malicious QR codes in public places to lead you to a fake website.',
                'option_c': 'A very quick and aggressive phishing attack that happens in real-time.',
                'option_d': 'A new type of antivirus software for mobile phones.',
                'correct_answer': 'b',
                'explanation': 'Quishing, or QR code phishing, uses malicious QR codes to lure victims to fake sites.'
            },
            {
                'question_text': 'What is the most important takeaway and best defense against constantly evolving threats like AI phishing and deepfakes?',
                'option_a': 'Only using one specific brand of antivirus software.',
                'option_b': 'Never opening any email from a person you don\'t know.',
                'option_c': 'Understanding that vigilance and continuous learning are essential because threats are always changing.',
                'option_d': 'Disconnecting from the internet when you see a threat you don\'t recognize.',
                'correct_answer': 'c',
                'explanation': 'Your vigilance and commitment to continuous learning are the best defense against evolving threats.'
            },
            {
                'question_text': 'Lesson 5.2 emphasizes building a "digital news habit." What is the main purpose of this habit?',
                'option_a': 'To learn how to predict when a cyberattack will happen, just like a weather forecast.',
                'option_b': 'To make cybersecurity a regular, lifelong practice of staying informed about new threats.',
                'option_c': 'To get daily news updates from the MMDC IT Helpdesk.',
                'option_d': 'To spend at least one hour every day reading about cybersecurity.',
                'correct_answer': 'b',
                'explanation': 'The goal is to make staying informed a regular, sustainable habit, not a one-time task.'
            },
            {
                'question_text': 'Which official Philippine government agency is mentioned for providing advisories on data breaches and online scams?',
                'option_a': 'The Hacker News',
                'option_b': 'The National Privacy Commission (NPC)',
                'option_c': 'The MMDC Student Affairs Office',
                'option_d': 'The Philstar Tech Section',
                'correct_answer': 'b',
                'explanation': 'The NPC is highlighted as an official government resource for local advisories and warnings.'
            },
            {
                'question_text': 'The program concludes by introducing "Digital Bayanihan." What does this mean?',
                'option_a': 'A government program that provides free cybersecurity software to students.',
                'option_b': 'A Filipino hacking group that targets scammers.',
                'option_c': 'The idea that protecting the community is a shared responsibility, where every student\'s actions contribute to the safety of others.',
                'option_d': 'A new social media platform exclusively for the MMDC community.',
                'correct_answer': 'c',
                'explanation': 'Digital Bayanihan is about shared, collective responsibility to protect each other online.'
            },
            {
                'question_text': '"One security breach can spread incredibly fast... Parang sakit." What security principle does this illustrate?',
                'option_a': 'That cybersecurity is only a personal responsibility.',
                'option_b': 'The importance of having fast internet.',
                'option_c': 'The collective impact, where one person\'s vulnerability can put the entire connected community at risk.',
                'option_d': 'That only the IT department can stop the spread of a threat.',
                'correct_answer': 'c',
                'explanation': 'This illustrates collective impact: one weak point can endanger the whole community.'
            },
            {
                'question_text': 'Which action best demonstrates the "Cyber Defender Mindset" taught in Lesson 5.3?',
                'option_a': 'Keeping quiet after spotting a phishing email to avoid causing panic.',
                'option_b': 'Blaming a classmate for falling for a scam.',
                'option_c': 'Politely speaking up in a group chat to warn others about a suspicious link that was shared.',
                'option_d': 'Assuming all QR codes in public places are safe to use.',
                'correct_answer': 'c',
                'explanation': 'A Cyber Defender takes proactive, responsible steps to protect others.'
            },
            {
                'question_text': 'What is the final and most important message of the program regarding your role?',
                'option_a': 'The best defense is to use the internet as little as possible.',
                'option_b': 'All security matters should be left to the IT department.',
                'option_c': 'Once you finish the program, you know everything you need to stay safe forever.',
                'option_d': 'You are not just a user; you are a defender with a personal and collective responsibility to keep the community safe.',
                'correct_answer': 'd',
                'explanation': 'Core pledge: You are a defender with responsibility to yourself and your community.'
            }
        ]

        for q in questions:
            row = KnowledgeCheckQuestion(
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                module_id=5,
                question_set=1
            )
            db.session.add(row)
        db.session.commit()
        return len(questions)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Default Module 5 KC seeding failed: {e}")
        return 0

# =============================================================================
# 10. ROUTE DEFINITIONS
# =============================================================================

# =============================================================================
# 10.1 AUTHENTICATION ROUTES
# =============================================================================

@app.route('/')
def index():
    """
    Home page route - displays the main landing page.
    
    Features:
    - Public access (no login required)
    - Responsive design with cybersecurity theme
    - Call-to-action buttons for registration/login
    - Program overview and features
    
    Returns:
        str: Rendered index.html template
    """
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        # Don't redirect to login on error, just show the page
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration route - handles new user account creation.
    
    Features:
    - Comprehensive form validation
    - Password strength requirements
    - Email format validation
    - Duplicate username/email checking
    - Secure password hashing
    - Automatic database initialization
    
    Methods:
        GET: Display registration form
        POST: Process registration data
        
    Returns:
        str: Rendered template or redirect
    """
    # Ensure database is initialized before processing registration
    try:
        with app.app_context():
            db.create_all()
            if Module.count() == 0:
                create_default_data()
                logger.info("[SUCCESS] Database auto-initialized during registration")
    except Exception as e:
        logger.error(f"[ERROR] Auto-database init during registration failed: {e}")
    
    if request.method == 'POST':
        try:
            # Get and validate form data
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            specialization = request.form.get('specialization', '')
            year_level = request.form.get('year_level', '')
            
            # Set default full name (can be updated in profile later)
            full_name = f"User {username}"
            
            # Validate required fields
            if not all([username, email, password, confirm_password, specialization, year_level]):
                flash('All fields are required.', 'error')
                logger.warning(f"Registration failed: Missing required fields for user {username}")
                return render_template('register.html', form_data=request.form)
            
            # Validate password confirmation
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                logger.warning(f"Registration failed: Password mismatch for user {username}")
                return render_template('register.html', form_data=request.form)
            
            # Create user data
            user_data = {
                'username': username,
                'email': email,
                'password': password,
                'full_name': full_name,
                'specialization': specialization,
                'year_level': year_level
            }
            
            try:
                user = user_service.create_user(user_data)
                if user:
                    flash('Registration successful! Please login.', 'success')
                    logger.info(f"User {username} registered successfully")
                    return redirect(url_for('login'))
            except ValueError as ve:
                flash(str(ve), 'error')
                logger.warning(f"Registration failed for user {username}: {ve}")
                
        except ValueError as e:
            flash(str(e), 'error')
            logger.error(f"Registration failed: {e}")
        except Exception as e:
            flash(f'Registration error: {e}', 'error')
            logger.error(f"Registration failed: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route - handles user authentication.
    
    Features:
    - Secure password verification
    - Session management
    - Login attempt logging
    - Redirect to dashboard on success
    - Automatic database initialization
    
    Methods:
        GET: Display login form
        POST: Process login credentials
        
    Returns:
        str: Rendered template or redirect
    """
    # Ensure database is initialized before processing login
    try:
        with app.app_context():
            db.create_all()
            if Module.count() == 0:
                create_default_data()
                logger.info("[SUCCESS] Database auto-initialized during login")
    except Exception as e:
        logger.error(f"[ERROR] Auto-database init during login failed: {e}")
    
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = user_service.authenticate_user(username, password)
            if user:
                login_user(user)
                flash('Login successful!', 'success')
                logger.info(f"User {username} logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
                logger.warning(f"Login failed for user {username}: Invalid credentials")
                
        except Exception as e:
            flash(f'Login error: {e}', 'error')
            logger.error(f"Login failed: {e}")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    User logout route - handles user session termination.
    
    Features:
    - Graceful logout for authenticated users
    - Session cleanup
    - Informative messages for different scenarios
    - No authentication required (fixes 500 error issue)
    
    Returns:
        str: Redirect to home page
    """
    try:
        if current_user.is_authenticated:
            username = current_user.username
            logout_user()
            flash('You have been logged out.', 'info')
            logger.info(f"User {username} logged out successfully")
        else:
            flash('You were already logged out.', 'info')
            logger.info("Logout attempted for non-authenticated user")
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        flash('Logout completed.', 'info')
    finally:
        # Clear any session data
        session.clear()
    
    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """
    Forgot password route - handles password reset requests.
    
    Features:
    - Email-based password reset
    - Token generation and validation
    - Security measures for reset process
    
    Returns:
        str: Rendered template or redirect
    """
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            if not email:
                flash('Please enter your email address.', 'error')
                return render_template('forgot_password.html')
            
            user = User.get_by_email(email)
            if user:
                # Generate reset token
                token = secrets.token_urlsafe(32)
                reset_token = PasswordResetToken(
                    user_id=user.id,
                    token=token,
                    expires_at=datetime.now() + timedelta(hours=24)
                )
                reset_token.save()
                
                # In a real application, send email here
                # For now, just show a success message
                flash('Password reset instructions have been sent to your email.', 'success')
                logger.info(f"Password reset requested for user {user.username}")
            else:
                # Don't reveal if email exists or not for security
                flash('If the email exists, password reset instructions have been sent.', 'info')
            
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            logger.error(f"Password reset error: {e}")
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Reset password route - handles password reset with token.
    
    Features:
    - Token validation
    - Password strength validation
    - Secure password update
    
    Args:
        token: Password reset token
        
    Returns:
        str: Rendered template or redirect
    """
    try:
        # Find valid reset token
        reset_token = PasswordResetToken.query.filter(
            PasswordResetToken.token == token,
            PasswordResetToken.expires_at > datetime.now(),
            PasswordResetToken.used == False
        ).first()
        
        if not reset_token:
            flash('Invalid or expired reset token.', 'error')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not password or not confirm_password:
                flash('Please fill in all fields.', 'error')
            elif password != confirm_password:
                flash('Passwords do not match.', 'error')
            elif len(password) < 12:
                flash('Password must be at least 12 characters long.', 'error')
            else:
                # Update user password
                user = User.get_by_id(reset_token.user_id)
                if user:
                    user.set_password(password)
                    user.save()
                    
                    # Mark token as used
                    reset_token.used = True
                    reset_token.save()
                    
                    flash('Password has been reset successfully. Please log in.', 'success')
                    logger.info(f"Password reset completed for user {user.username}")
                    return redirect(url_for('login'))
        
        return render_template('reset_password.html', token=token)
        
    except Exception as e:
        flash('An error occurred. Please try again.', 'error')
        logger.error(f"Password reset error: {e}")
        return redirect(url_for('login'))

# =============================================================================
# 10.2 LEARNING ROUTES
# =============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard route - displays user progress and learning overview.
    
    Features:
    - Comprehensive progress tracking
    - Module completion status
    - Recent activity feed
    - Performance analytics
    - Access control for modules
    
    Returns:
        str: Rendered dashboard template
    """
    try:
        # Get user statistics using service
        user_stats = user_service.get_user_statistics(current_user.id)
        
        # Get user progress
        user_progress = UserProgress.get_user_progress(current_user.id)
        
        # Get modules
        modules = Module.get_all_ordered()
        
        # Get total modules count
        total_modules = Module.count() if modules else 0
        
        # Get properly completed modules using validation
        completed_module_ids = user_service.get_user_completed_modules(current_user.id)
        completed_modules = len(completed_module_ids)
        
        # Get final assessment result
        final_result = AssessmentResult.query.filter_by(
            user_id=current_user.id, 
            assessment_type='final_assessment', 
            passed=True
        ).first()
        
        # Get survey completion status
        survey_completed = FeedbackSurvey.query.filter_by(user_id=current_user.id).first()
        
        # Calculate accessible modules (modules 1 to total_modules)
        accessible_modules = []
        for i in range(1, total_modules + 1):  # Modules 1 to total_modules
            if i == 1:
                # First module is always accessible
                accessible_modules.append(True)
            elif current_user.is_admin:
                # Administrators can access all modules for testing and review
                accessible_modules.append(True)
            else:
                # Other modules are accessible if previous module is fully completed
                previous_module_completed = user_service.is_module_fully_completed(current_user.id, i-1)
                accessible_modules.append(previous_module_completed)
        
        # Build recent activity feed (simulations, assessments, module completions, surveys)
        recent_activities = []

        # Simulations
        sim_results = SimulationResult.query.filter_by(
            user_id=current_user.id
        ).order_by(SimulationResult.created_at.desc()).limit(10).all()
        for sim in sim_results:
            recent_activities.append({
                'type': 'simulation',
                'title': f"{(sim.simulation_type or '').replace('_', ' ').title()} Simulation",
                'detail': f"Score: {sim.score}%",
                'badge_text': 'Completed' if sim.completed else 'In Progress',
                'badge_class': 'bg-success' if sim.completed else 'bg-warning',
                'timestamp': sim.updated_at or sim.created_at
            })

        # Assessments (knowledge checks, final, baseline)
        assess_results = AssessmentResult.query.filter_by(user_id=current_user.id)\
            .order_by(AssessmentResult.created_at.desc()).limit(10).all()
        for ar in assess_results:
            module_name = None
            if ar.module_id:
                m = Module.get_by_id(ar.module_id)
                module_name = m.name if m else None
            assessment_label = {
                'knowledge_check': 'Knowledge Check',
                'final_assessment': 'Final Assessment',
                'baseline': 'Baseline Assessment',
                'follow_up': 'Follow-up Assessment'
            }.get(ar.assessment_type, 'Assessment')
            title = f"{assessment_label}" + (f" - {module_name}" if module_name else '')
            percent = int((ar.score / ar.total_questions) * 100) if ar.total_questions and ar.total_questions > 0 else ar.score
            recent_activities.append({
                'type': 'assessment',
                'title': title,
                'detail': f"Score: {percent}% ({ar.correct_answers}/{ar.total_questions})",
                'badge_text': 'Passed' if getattr(ar, 'passed', False) else 'Failed',
                'badge_class': 'bg-success' if getattr(ar, 'passed', False) else 'bg-danger',
                'timestamp': ar.created_at
            })

        # Module completions
        completed_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            status='completed'
        ).order_by(UserProgress.completed_at.desc()).limit(10).all()
        for up in completed_progress:
            m = Module.get_by_id(up.module_id)
            recent_activities.append({
                'type': 'module',
                'title': f"Module Completed - {m.name if m else f'ID {up.module_id}'}",
                'detail': f"Score: {up.score}%",
                'badge_text': 'Completed',
                'badge_class': 'bg-success',
                'timestamp': up.completed_at or up.updated_at or up.created_at
            })

        # Surveys
        surveys = FeedbackSurvey.query.filter_by(user_id=current_user.id)\
            .order_by(FeedbackSurvey.created_at.desc()).limit(10).all()
        for s in surveys:
            m = Module.get_by_id(s.module_id) if s.module_id else None
            recent_activities.append({
                'type': 'survey',
                'title': f"Feedback Submitted" + (f" - {m.name}" if m else ''),
                'detail': f"Rating: {s.rating}/5",
                'badge_text': 'Submitted',
                'badge_class': 'bg-info',
                'timestamp': s.created_at
            })

        # Sort by timestamp and take top 5
        recent_activities = sorted(
            recent_activities,
            key=lambda a: a['timestamp'] or datetime.utcnow(),
            reverse=True
        )[:5]
        
        # Calculate average score from assessment results
        assessment_results = AssessmentResult.query.filter_by(user_id=current_user.id).all()
        if assessment_results:
            total_score = sum(result.score for result in assessment_results)
            total_questions = sum(result.total_questions for result in assessment_results)
            average_score = int((total_score / total_questions) * 100) if total_questions and total_questions > 0 else 0
        else:
            average_score = 0
        
        # Calculate total time spent using real tracked minutes; fall back safely
        total_time_spent = 0
        try:
            if user_stats:
                # Prefer explicit aggregate minutes from service
                total_time_spent = (
                    user_stats.get('total_time_spent')
                    or (user_stats.get('time_analytics', {}) or {}).get('total_time_spent_minutes')
                    or 0
                )
            if not total_time_spent:
                # Fallback: sum from in-memory progress list
                total_time_spent = sum((p.time_spent or 0) for p in (user_progress or []))
        except Exception:
            # Last resort: retain previous estimate so UI never breaks
            total_time_spent = completed_modules * 30
        
        # Ensure all variables are safe for template rendering
        safe_user_stats = user_stats or {}
        safe_user_progress = user_progress or []
        safe_modules = modules or []
        safe_recent_activities = recent_activities or []
        
        return render_template('dashboard.html', 
                             user_stats=safe_user_stats,
                             user_progress=safe_user_progress,
                             modules=safe_modules,
                             completed_modules=completed_modules,
                             completed_module_ids=completed_module_ids,
                             total_modules=total_modules,
                             final_result=final_result,
                             survey_completed=survey_completed,
                             accessible_modules=accessible_modules,
                             recent_activities=safe_recent_activities,
                             average_score=average_score,
                             total_time_spent=total_time_spent)
    except Exception as e:
        flash(f'Error loading dashboard: {e}', 'error')
        logger.error(f"Error loading dashboard: {e}")
        # Return a minimal dashboard with safe defaults
        try:
            return render_template('dashboard.html', 
                                 user_stats={},
                                 user_progress=[],
                                 modules=[],
                                 completed_modules=0,
                                 completed_module_ids=[],
                                 total_modules=0,
                                 final_result=None,
                                 survey_completed=None,
                                 accessible_modules=[],
                                 recent_activities=[],
                                 average_score=0,
                                 total_time_spent=0)
        except Exception as template_error:
            logger.error(f"Template rendering error: {template_error}")
        return redirect(url_for('index'))

@app.route('/module/<int:module_id>')
@login_required
def module(module_id):
    """
    Module view route - displays educational content for a specific module.
    
    Features:
    - Progressive module access control
    - Interactive content display
    - Progress tracking
    - Knowledge check integration
    - Simulation access for applicable modules
    
    Args:
        module_id (int): ID of the module to display
        
    Returns:
        str: Rendered module template or redirect
    """
    try:
        module_obj = Module.get_by_id(module_id)
        if not module_obj:
            flash('Module not found.', 'error')
            logger.warning(f"Module {module_id} not found")
            return redirect(url_for('dashboard'))
            
        # Check if user can access this module
        if module_id == 1:
            # First module is always accessible
            pass
        elif current_user.is_admin:
            # Administrators can access all modules for testing and review
            pass
        else:
            # Check if previous module is fully completed for regular users
            previous_module_completed = user_service.is_module_fully_completed(current_user.id, module_id - 1)
            if not previous_module_completed:
                flash('You must complete the previous module before accessing this one.', 'warning')
                logger.warning(f"User {current_user.username} attempted to access module {module_id} without completing module {module_id - 1}")
                return redirect(url_for('dashboard'))
        
        # Get user progress for this module
        progress = UserProgress.get_module_progress(current_user.id, module_id)
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                module_id=module_id,
                status='not_started'
            )
            progress.save()
        
        # Get knowledge check score for this module
        knowledge_check_result = AssessmentResult.query.filter_by(
            user_id=current_user.id,
            module_id=module_id,
            assessment_type='knowledge_check'
        ).order_by(AssessmentResult.created_at.desc()).first()
        
        # Calculate percentage score
        if knowledge_check_result and knowledge_check_result.total_questions and knowledge_check_result.total_questions > 0:
            knowledge_check_score = int((knowledge_check_result.score / knowledge_check_result.total_questions) * 100)
        else:
            knowledge_check_score = 0

        # Reconcile progress status with policy: mark Completed at ≥80% and never downgrade
        try:
            passing_threshold = app.config.get('KNOWLEDGE_CHECK_PASSING_SCORE', 80)
            if progress and knowledge_check_score >= passing_threshold and progress.status != 'completed':
                # Use model helper to persist the completion state safely
                progress.complete_progress(knowledge_check_score)
        except Exception as _e:
            logger.warning(f"Could not reconcile module progress for user {current_user.id} module {module_id}: {_e}")
        
        return render_template('module.html', 
                             module=module_obj,
                             progress=progress, 
                             knowledge_check_score=knowledge_check_score)
    except Exception as e:
        flash(f'Error loading module: {e}', 'error')
        logger.error(f"Error loading module {module_id}: {e}")
        return redirect(url_for('dashboard'))

# =============================================================================
# 10.3 ASSESSMENT ROUTES
# =============================================================================

@app.route('/assessment/<int:module_id>')
@login_required
def assessment(module_id):
    """
    Module assessment route - displays knowledge check for a specific module.
    
    Features:
    - Dynamic question generation
    - Progress validation
    - Access control
    - Assessment state management
    
    Args:
        module_id (int): ID of the module for assessment
        
    Returns:
        str: Rendered assessment template or redirect
    """
    try:
        # Get module
        module_obj = Module.get_by_id(module_id)
        if not module_obj:
            flash('Module not found.', 'error')
            return redirect(url_for('dashboard'))
        
        # Check if user can access this module
        if module_id > 1 and not current_user.is_admin:
            # Regular users must complete previous module; administrators have full access
            previous_module_completed = user_service.is_module_fully_completed(current_user.id, module_id - 1)
            if not previous_module_completed:
                flash('You must complete the previous module first.', 'warning')
                return redirect(url_for('dashboard'))
        
        # Get questions for this module with retake logic
        # Check if user has previous attempts to determine question set
        previous_attempts = AssessmentResult.query.filter_by(
            user_id=current_user.id,
            module_id=module_id,
            assessment_type='knowledge_check'
        ).count()
        
        # Use different question sets for retakes (1, 2, 1, 2, etc.)
        question_set = (previous_attempts % 2) + 1
        
        # Get questions from the determined set
        questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
        # If module 3 has no questions yet, seed defaults once
        if module_id == 3 and not questions:
            inserted = seed_module3_kc_default()
            if inserted > 0:
                questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
        
        # If no questions in this set, try all questions; if still none, auto-seed defaults for specific modules
        if not questions:
            questions = KnowledgeCheckQuestion.query.filter_by(module_id=module_id).all()
            if not questions:
                try:
                    if module_id == 1:
                        # from learning_modules.module1 import Module1Questions
                        def _normalize(q: dict, set_num: int) -> dict:
                            return {
                                'question_text': q.get('question_text') or q.get('question') or '',
                                'option_a': q.get('option_a', ''),
                                'option_b': q.get('option_b', ''),
                                'option_c': q.get('option_c', ''),
                                'option_d': q.get('option_d', ''),
                                'correct_answer': q.get('correct_answer', ''),
                                'explanation': q.get('explanation', ''),
                                'module_id': 1,
                                'question_set': set_num
                            }
                        # Seed from both sets - TEMPORARILY DISABLED
                        # for q in Module1Questions.get_question_set_1():
                        #     db.session.add(KnowledgeCheckQuestion(**_normalize(q, 1)))
                        # for q in Module1Questions.get_question_set_2():
                        #     db.session.add(KnowledgeCheckQuestion(**_normalize(q, 2)))
                        db.session.commit()
                        # Re-query
                        questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
                        if not questions:
                            # As a final fallback, seed a default curated set for Module 1
                            inserted = seed_module1_kc_default()
                            if inserted > 0:
                                questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
                    elif module_id == 4:
                        inserted = seed_module4_kc_default()
                        if inserted > 0:
                            questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
                    elif module_id == 5:
                        inserted = seed_module5_kc_default()
                        if inserted > 0:
                            questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
                except Exception as seed_err:
                    logger.error(f"Auto-seed questions failed for module {module_id}: {seed_err}")
            if not questions:
                flash('No questions available for this module.', 'error')
                return redirect(url_for('module', module_id=module_id))
        
        # Shuffle questions for variety and enforce 5-question rule
        random.shuffle(questions)
        if len(questions) > 5:
            questions = questions[:5]
        
        return render_template('assessment_simple.html',
                             module=module_obj,
                             questions=questions,
                             module_id=module_id)
    except Exception as e:
        flash(f'Error loading assessment: {e}', 'error')
        logger.error(f"Error loading assessment for module {module_id}: {e}")
        return redirect(url_for('dashboard'))

@app.route('/submit_assessment/<int:module_id>', methods=['POST'])
@login_required
def submit_assessment(module_id):
    """
    Submit assessment answers and calculate results.
    
    Features:
    - Answer validation and scoring
    - Progress tracking
    - Detailed feedback
    - Result storage
    
    Args:
        module_id (int): ID of the module for assessment
        
    Returns:
        str: Rendered result template or redirect
    """
    try:
        # Debug: Log the module_id parameter
        logger.info(f"submit_assessment called with module_id: {module_id}")
        
        # Get module
        module_obj = Module.get_by_id(module_id)
        if not module_obj:
            flash('Module not found.', 'error')
            return redirect(url_for('dashboard'))
        
        # Get questions for this module
        # If the form sends explicit question_ids, grade only those
        submitted_question_ids = request.form.get('question_ids')
        if submitted_question_ids:
            try:
                id_list = [int(qid) for qid in submitted_question_ids.split(',') if qid.strip()]
            except Exception:
                id_list = []
        else:
            id_list = []

        if id_list:
            questions = KnowledgeCheckQuestion.query.filter(KnowledgeCheckQuestion.id.in_(id_list)).all()
        else:
            # Use assessment route logic: choose set based on prior attempts, then select first 5
            previous_attempts = AssessmentResult.query.filter_by(
                user_id=current_user.id,
                module_id=module_id,
                assessment_type='knowledge_check'
            ).count()
            question_set = (previous_attempts % 2) + 1
            questions = KnowledgeCheckQuestion.get_by_module_and_set(module_id, question_set)
            import random
            random.shuffle(questions)
            if len(questions) > 5:
                questions = questions[:5]
        if not questions:
            flash('No questions available for this module.', 'error')
            return redirect(url_for('module', module_id=module_id))
        
        # Process answers
        answers = {}
        correct_answers = 0
        total_questions = len(questions)
        
        detailed_results = []
        for question in questions:
            answer = request.form.get(f'question_{question.id}')
            answers[question.id] = answer
            
            is_correct = (answer == question.correct_answer)
            if is_correct:
                correct_answers += 1
            
            # Build question-level feedback for review
            try:
                detailed_results.append({
                    'question_text': getattr(question, 'question_text', getattr(question, 'question', '')),
                    'user_answer': (answer or ''),
                    'correct_answer': getattr(question, 'correct_answer', ''),
                    'explanation': getattr(question, 'explanation', ''),
                    'is_correct': is_correct
                })
            except Exception:
                # Fail-safe in case fields are missing
                detailed_results.append({
                    'question_text': '',
                    'user_answer': (answer or ''),
                    'correct_answer': '',
                    'explanation': '',
                    'is_correct': is_correct
                })
        
        # Calculate score
        score = correct_answers
        percentage = (correct_answers / total_questions) * 100 if total_questions and total_questions > 0 else 0
        
        # Determine if passed (80% threshold)
        passed = percentage >= app.config.get('KNOWLEDGE_CHECK_PASSING_SCORE', 80)
        
        # Create assessment result
        result = AssessmentResult(
            user_id=current_user.id,
            module_id=module_id,
            assessment_type='knowledge_check',
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            passed=passed
        )
        
        if result.save():
            # Update module progress with "Pass Once, Always Complete" rule
            progress = UserProgress.get_module_progress(current_user.id, module_id)
            if progress:
                # Use the new update_score method that implements the rule
                progress.update_score(percentage)
            else:
                # Create new progress record
                progress = UserProgress(
                    user_id=current_user.id,
                    module_id=module_id,
                    status='in_progress'
                )
                progress.save()
                progress.update_score(percentage)
            
            flash(f'Assessment completed! Score: {percentage}%', 'success' if passed else 'warning')
            logger.info(f"User {current_user.username} completed assessment for module {module_id} with score {percentage}%")
            
            # Debug: Log template variables before rendering
            logger.info(f"Rendering assessment_result.html with module_id: {module_id}, module_obj: {module_obj}")
            
            return render_template('assessment_result.html',
                                     module=module_obj,
                                     module_id=module_id,
                                     score=correct_answers,
                                     total_questions=total_questions,
                                     percentage=percentage,
                                     correct_answers=correct_answers,
                                     passed=passed,
                                     detailed_results=detailed_results,
                                     questions=questions,
                                     answers=answers)
        else:
            flash('Error saving assessment results.', 'error')
            return redirect(url_for('module', module_id=module_id))
        
    except Exception as e:
        flash(f'Error submitting assessment: {e}', 'error')
        logger.error(f"Error submitting assessment for module {module_id}: {e}")
        return redirect(url_for('dashboard'))

# =============================================================================
# 10.4 FINAL ASSESSMENT ROUTES
# =============================================================================

@app.route('/final_assessment')
@login_required
def final_assessment():
    """
    Final assessment route - displays the comprehensive final assessment.
    
    Features:
    - Access control (only after completing all modules)
    - Comprehensive question set
    - Time tracking
    - Certificate eligibility
    
    Returns:
        str: Rendered final assessment template or redirect
    """
    try:
        # Check if user has completed all modules (admins bypass for review)
        completed_modules = len(user_service.get_user_completed_modules(current_user.id))
        total_modules = Module.count()
        
        if not getattr(current_user, 'is_admin', False):
            if completed_modules < total_modules:
                flash('You must complete all modules before taking the Final Assessment.', 'warning')
                return redirect(url_for('dashboard'))
        else:
            # For admins, present as fully completed to unlock UI state
            completed_modules = total_modules
        
        # Check if user has already passed (allow retakes for better scores)
        existing_result = AssessmentResult.query.filter_by(
            user_id=current_user.id, 
            assessment_type='final_assessment',
            passed=True
        ).first()
        
        if existing_result:
            flash('You have already passed the Final Assessment! You can retake for a better score.', 'info')
        
        return render_template('final_assessment_simple.html',
                               completed_modules=completed_modules,
                               total_modules=total_modules)
        
    except Exception as e:
        flash(f'Error loading final assessment: {e}', 'error')
        logger.error(f"Error loading final assessment: {e}")
        return redirect(url_for('dashboard'))

@app.route('/final_assessment_questions')
@login_required
def final_assessment_questions():
    """
    Final assessment questions route - displays the actual assessment.
    
    Returns:
        str: Rendered final assessment questions template
    """
    try:
        # Get final assessment questions — policy: show 25 questions per attempt
        # Load all questions for the chosen set, then sample 25 consistently with utils
        questions_all = FinalAssessmentQuestion.query.all()
        if not questions_all:
            flash('No final assessment questions available.', 'error')
            return redirect(url_for('dashboard'))
        import random
        random.shuffle(questions_all)
        questions = questions_all[:25]
        # Render 25 questions per policy
        return render_template('final_assessment_questions.html', questions=questions)
        
    except Exception as e:
        flash(f'Error loading final assessment questions: {e}', 'error')
        logger.error(f"Error loading final assessment questions: {e}")
        return redirect(url_for('dashboard'))

@app.route('/submit_final_assessment', methods=['POST'])
@login_required
def submit_final_assessment():
    """
    Submit final assessment answers and calculate results.
    
    Returns:
        str: Rendered result template or redirect
    """
    try:
        # Get questions — must match the 25 displayed
        # If explicit question_ids posted, honor them
        submitted_question_ids = request.form.get('question_ids')
        if submitted_question_ids:
            try:
                id_list = [int(qid) for qid in submitted_question_ids.split(',') if qid.strip()]
            except Exception:
                id_list = []
        else:
            id_list = []

        if id_list:
            questions = FinalAssessmentQuestion.query.filter(FinalAssessmentQuestion.id.in_(id_list)).all()
        else:
            # Fallback: sample 25 consistently as in questions route
            questions_all = FinalAssessmentQuestion.query.all()
            if not questions_all:
                flash('No final assessment questions available.', 'error')
                return redirect(url_for('dashboard'))
            import random
            random.shuffle(questions_all)
            questions = questions_all[:25]
        if not questions:
            flash('No final assessment questions available.', 'error')
            return redirect(url_for('dashboard'))
        
        # Process answers
        answers = {}
        correct_answers = 0
        total_questions = len(questions)
        
        for question in questions:
            answer = request.form.get(f'question_{question.id}')
            answers[question.id] = answer
            
            if answer == question.correct_answer:
                correct_answers += 1
        
        # Calculate score
        score = correct_answers
        percentage = int((correct_answers / total_questions) * 100) if total_questions and total_questions > 0 else 0
        
        # Determine if passed (80% threshold for final assessment)
        passed = percentage >= app.config.get('FINAL_ASSESSMENT_PASSING_SCORE', 80)
        
        # Create assessment result
        result = AssessmentResult(
            user_id=current_user.id,
            module_id=None,  # Final assessment is not tied to a specific module
            assessment_type='final_assessment',
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            passed=passed
        )
        
        if result.save():
            flash(f'Final Assessment completed! Score: {percentage}%', 'success' if passed else 'warning')
            logger.info(f"User {current_user.username} completed final assessment with score {percentage}%")
            
            return render_template('final_assessment_result.html',
                                     score=correct_answers,
                                     total_questions=total_questions,
                                     correct_answers=correct_answers,
                                     percentage=percentage,
                                     passed=passed,
                                     detailed_results=[],
                                     questions=questions,
                                     answers=answers)
        else:
            flash('Error saving final assessment results.', 'error')
            return redirect(url_for('final_assessment'))
        
    except Exception as e:
        flash(f'Error submitting final assessment: {e}', 'error')
        logger.error(f"Error submitting final assessment: {e}")
        return redirect(url_for('dashboard'))

# =============================================================================
# 10.5 SURVEY AND CERTIFICATE ROUTES
# =============================================================================

@app.route('/survey')
@login_required
def survey():
    """
    Program survey route - displays feedback survey.
    
    Returns:
        str: Rendered survey template
    """
    try:
        # Allow admins to access survey without prerequisites
        if getattr(current_user, 'is_admin', False):
            return render_template('survey.html')

        # Check if user has passed final assessment
        final_result = AssessmentResult.query.filter_by(
            user_id=current_user.id,
            assessment_type='final_assessment',
            passed=True
        ).first()
        
        if not final_result:
            flash('You must pass the Final Assessment before taking the survey.', 'warning')
            return redirect(url_for('dashboard'))
        
        # Check if survey already completed
        existing_survey = FeedbackSurvey.query.filter_by(user_id=current_user.id).first()
        if existing_survey:
            flash('You have already completed the survey.', 'info')
            return redirect(url_for('dashboard'))
        
        return render_template('survey.html')
        
    except Exception as e:
        flash(f'Error loading survey: {e}', 'error')
        logger.error(f"Error loading survey: {e}")
        return redirect(url_for('dashboard'))

@app.route('/api/submit-survey', methods=['POST'])
@login_required
def api_submit_survey():
    """JSON survey submission used by the in‑app survey page.

    Expects a JSON body with 1–5 ratings for ~10 questions plus an optional
    free‑text suggestion. Saves core rating/difficulty and packs the rest
    into FeedbackSurvey.additional_questions for easy aggregation.
    """
    try:
        data = request.get_json(silent=True) or {}

        # Core, required rating (fallback to 0 if missing)
        rating = int(data.get('overall_quality') or data.get('rating') or 0)
        difficulty_level = (data.get('difficulty_level') or '').strip() or None
        suggestion = (data.get('feedback') or '').strip()

        # Collect numeric answers for analysis
        question_keys = [
            'content_relevance',
            'simulations_helpful',
            'confidence_identify_attacks',
            'content_clarity',
            'module_flow',
            'ui_usability',
            'video_helpfulness',
            'knowledge_check_fairness',
            'final_assessment_fairness',
            'recommendation_intent'
        ]
        additional = {}
        for key in question_keys:
            val = data.get(key)
            if isinstance(val, (int, float)):
                additional[key] = int(val)
            elif isinstance(val, str) and val.isdigit():
                additional[key] = int(val)

        survey = FeedbackSurvey(
            user_id=current_user.id,
            rating=rating,
            feedback_text=suggestion if suggestion else None,
            difficulty_level=difficulty_level
        )
        if additional:
            survey.set_additional_questions(additional)

        if survey.save():
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to save survey.'}), 400
    except Exception as e:
        logger.error(f"Error submitting survey (API): {e}")
        return jsonify({'success': False, 'error': 'Server error'}), 500

@app.route('/submit_survey', methods=['POST'])
@login_required
def submit_survey():
    """
    Submit survey responses.
    
    Returns:
        str: Redirect to certificate or dashboard
    """
    try:
        # Get survey data
        rating = request.form.get('rating', type=int)
        feedback = request.form.get('feedback', '')
        
        # Create survey record
        survey = FeedbackSurvey(
            user_id=current_user.id,
            rating=rating,
            feedback=feedback
        )
        
        if survey.save():
            flash('Survey submitted successfully!', 'success')
            logger.info(f"User {current_user.username} completed survey")
            return redirect(url_for('certificate'))
        else:
            flash('Error saving survey.', 'error')
            return redirect(url_for('survey'))
        
    except Exception as e:
        flash(f'Error submitting survey: {e}', 'error')
        logger.error(f"Error submitting survey: {e}")
        return redirect(url_for('survey'))

@app.route('/certificate')
@login_required
def certificate():
    """
    Certificate generation route.
    
    Returns:
        str: Rendered certificate template
    """
    try:
        # Admin bypass: allow viewing the certificate page for testing
        is_admin = getattr(current_user, 'is_admin', False)

        # Enforce profile full name requirement (non-admins)
        try:
            full_name = (getattr(current_user, 'full_name', None) or '').strip()
        except Exception:
            full_name = ''
        def _is_valid_full_name(name: str) -> bool:
            return bool(name) and (' ' in name) and (len(name) >= 5)
        if not is_admin and not _is_valid_full_name(full_name):
            flash('Please complete your full name in your Profile before generating a certificate.', 'warning')
            return redirect(url_for('profile'))

        # Check eligibility only for non-admins
        # Admins can view for QA even without prerequisites
        final_result = AssessmentResult.query.filter_by(
            user_id=current_user.id,
            assessment_type='final_assessment',
            passed=True
        ).first()
        
        survey_completed = FeedbackSurvey.query.filter_by(user_id=current_user.id).first()
        
        if not is_admin and not final_result:
            flash('You must pass the Final Assessment to generate a certificate.', 'warning')
            return redirect(url_for('dashboard'))
        
        if not is_admin and not survey_completed:
            flash('You must complete the survey to generate a certificate.', 'warning')
            return redirect(url_for('survey'))

        # Build minimal certificate context to avoid undefined errors
        try:
            completed_modules = len(user_service.get_user_completed_modules(current_user.id))
        except Exception:
            completed_modules = 0

        try:
            results = AssessmentResult.query.filter_by(user_id=current_user.id).all()
            total_q = sum((r.total_questions or 0) for r in results)
            total_s = sum((r.score or 0) for r in results)
            avg_score = int((total_s / total_q) * 100) if total_q else 0
        except Exception:
            avg_score = 0

        certificate_data = {
            'student_name': getattr(current_user, 'full_name', None) or getattr(current_user, 'username', 'Student'),
            'username': getattr(current_user, 'username', 'student'),
            'specialization': getattr(current_user, 'specialization', None) or '—',
            'year_level': getattr(current_user, 'year_level', None) or '—',
            'completion_date': datetime.utcnow().strftime('%B %d, %Y, %I:%M %p'),
            'modules_completed': completed_modules,
            'score': avg_score,
            # Certificate ID format: MMDCSEA-[MMDDYYYY]0000001 (use user id zero-padded to 7 digits)
            'certificate_id': f"MMDCSEA-{datetime.utcnow().strftime('%m%d%Y')}{str(getattr(current_user, 'id', 1)).zfill(7)}"
        }

        return render_template('certificate.html', certificate=certificate_data)
        
    except Exception as e:
        flash(f'Error generating certificate: {e}', 'error')
        logger.error(f"Error generating certificate: {e}")
        return redirect(url_for('dashboard'))

# =============================================================================
# 10.6 SIMULATION ROUTES
# =============================================================================

@app.route('/simulation/<simulation_type>')
@login_required
def simulation(simulation_type):
    """
    Simulation route - displays interactive social engineering scenarios.
    
    Features:
    - Dynamic scenario generation
    - Real-time feedback
    - Progress tracking
    - Educational content integration
    
    Args:
        simulation_type (str): Type of simulation (phishing, pretexting, etc.)
        
    Returns:
        str: Rendered simulation template or redirect
    """
    try:
        # Validate simulation type
        valid_types = ['phishing', 'pretexting', 'baiting', 'quid_pro_quo']
        if simulation_type not in valid_types:
            flash('Invalid simulation type.', 'error')
            return redirect(url_for('dashboard'))
        
        # Get simulation data
        simulation_data = simulation_service.get_simulation_data(simulation_type)
        if not simulation_data:
            flash('Simulation not available.', 'error')
            return redirect(url_for('dashboard'))
        
        return render_template('simulation_simple.html', 
                             simulation_type=simulation_type,
                             content=simulation_data)
    except Exception as e:
        flash(f'Error loading simulation: {e}', 'error')
        logger.error(f"Error loading simulation {simulation_type}: {e}")
        return redirect(url_for('dashboard'))

@app.route('/submit_simulation', methods=['POST'])
@login_required
def submit_simulation():
    """
    Submit simulation responses and calculate results.
    
    Features:
    - Response evaluation
    - Learning feedback
    - Score calculation
    - Progress tracking
    
    Returns:
        str: JSON response with results
    """
    try:
        simulation_type = request.form.get('simulation_type')
        responses = request.form.get('responses', '{}')
        
        # Parse responses
        try:
            responses = json.loads(responses)
        except json.JSONDecodeError:
            responses = {}
        
        # Evaluate simulation
        result = simulation_service.evaluate_simulation(
            current_user.id, 
            simulation_type, 
            responses
        )
        
        if result:
            flash('Simulation completed successfully!', 'success')
            return jsonify({
                'success': True,
                'score': result.score,
                'feedback': result.feedback
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to evaluate simulation'
            })
            
    except Exception as e:
        logger.error(f"Error submitting simulation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

# =============================================================================
# 10.7 PROGRESS AND ANALYTICS ROUTES
# =============================================================================

@app.route('/profile')
@login_required
def profile():
    """
    User profile route - displays and manages user profile information.
    
    Features:
    - Profile information display
    - Edit capabilities
    - Progress overview
    - Achievement tracking
    
    Returns:
        str: Rendered profile template
    """
    try:
        return render_template('profile.html', user=current_user)
    except Exception as e:
        flash(f'Error loading profile: {e}', 'error')
        logger.error(f"Error loading profile: {e}")
        return redirect(url_for('dashboard'))

@app.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    """
    Update user progress for modules and activities.
    
    Features:
    - Progress tracking
    - Time spent calculation
    - Status updates
    - Completion validation
    
    Returns:
        str: JSON response with update status
    """
    try:
        # Support both JSON and form-encoded payloads
        payload = request.get_json(silent=True) or {}
        module_id = payload.get('module_id') if payload else request.form.get('module_id', type=int)
        try:
            module_id = int(module_id) if module_id is not None else None
        except Exception:
            module_id = None
        status = (payload.get('status') if payload else request.form.get('status')) or 'in_progress'
        try:
            score = int(payload.get('score', 0) if payload else request.form.get('score', 0))
        except Exception:
            score = 0
        try:
            time_spent = int(payload.get('time_spent', 0) if payload else request.form.get('time_spent', 0))
        except Exception:
            time_spent = 0
        
        if not module_id:
            return jsonify({'success': False, 'error': 'Module ID required'})
        
        # Get or create progress record
        progress = UserProgress.get_module_progress(current_user.id, module_id)
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                module_id=module_id,
                status='not_started'
            )

        # Update progress (always apply updates)
        progress.status = status
        progress.score = score
        progress.time_spent = time_spent
        
        if progress.save():
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to save progress'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# =============================================================================
# 10.8 SYSTEM ROUTES
# =============================================================================

@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring and deployment verification.
    
    Features:
    - Database connectivity check
    - Application status
    - Version information
    - Timestamp for monitoring
    
    Returns:
        str: JSON response with health status
    """
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'version': '1.0.0'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/learning_assets/<path:filename>')
def learning_assets(filename):
    """
    Serve learning assets (e.g., images, PDFs) from approved subdirectories
    under learning_modules. Supports nested paths like 'Visual_Aid/Lesson21.png'.
    """
    try:
        import os
        app_root = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(app_root, 'learning_modules')

        # Only allow serving from these subdirectories
        allowed_subdirs = ['Documents', 'Visual_Aid']

        # If the filename already contains a subdirectory, try to serve directly
        # from an allowed subdirectory. Otherwise, try each allowed subdir.
        for subdir in allowed_subdirs:
            candidate_dir = os.path.join(base_dir, subdir)
            candidate_path = os.path.join(candidate_dir, filename)
            if os.path.isfile(candidate_path):
                return send_from_directory(candidate_dir, filename)

        # As a fallback, if a fully qualified path under base_dir was provided and exists
        fallback_path = os.path.join(base_dir, filename)
        if os.path.isfile(fallback_path):
            # Determine the directory and relative file for send_from_directory
            rel_dir = os.path.dirname(fallback_path)
            rel_file = os.path.basename(fallback_path)
            return send_from_directory(rel_dir, rel_file)

        # Not found
        return ('', 404)
    except Exception as e:
        logger.error(f"Error serving learning asset {filename}: {e}")
        return ('', 404)

@app.route('/init-db')
def init_database_route():
    """
    Database initialization endpoint for Render deployment.
    
    This endpoint ensures the database is properly initialized
    when the application starts on Render.
    
    Returns:
        str: JSON response with initialization status
    """
    try:
        with app.app_context():
            init_database()
        return jsonify({
            'status': 'success',
            'message': 'Database initialized successfully',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# =============================================================================
# 11. ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors.
    
    Args:
        error: The 404 error object
        
    Returns:
        str: Rendered 404 error page
    """
    logger.warning(f"404 error: {error}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server errors.
    
    Features:
    - Database rollback on errors
    - Error logging
    - User-friendly error page
    
    Args:
        error: The 500 error object
        
    Returns:
        str: Rendered 500 error page
    """
    db.session.rollback()
    logger.error(f"500 error: {error}")
    return render_template('500.html'), 500

# =============================================================================
# 12. ADMIN DASHBOARD ROUTES
# =============================================================================

def admin_required(f):
    """Decorator to require admin access"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access admin panel.', 'error')
            return redirect(url_for('login'))
        
        # Check if user is admin (simple check for now)
        if current_user.username != 'administrator':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard main page"""
    try:
        # Get system statistics
        total_users = User.count()
        total_modules = Module.query.filter(Module.id <= 6).count()  # Count all modules including Final Assessment
        total_assessments = AssessmentResult.count()
        total_simulations = SimulationResult.count()
        
        # Get recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        recent_assessments = AssessmentResult.query.order_by(AssessmentResult.created_at.desc()).limit(10).all()
        recent_reflections = SimpleReflection.query.order_by(SimpleReflection.created_at.desc()).limit(20).all()
        
        # Get user statistics
        users_by_specialization = db.session.query(
            User.specialization, 
            db.func.count(User.id)
        ).group_by(User.specialization).all()
        
        users_by_year = db.session.query(
            User.year_level,
            db.func.count(User.id)
        ).group_by(User.year_level).all()
        
        # Aggregate simple survey summary from FeedbackSurvey
        try:
            surveys = FeedbackSurvey.query.order_by(FeedbackSurvey.created_at.desc()).all()
            count = len(surveys)
            def avg(getter):
                vals = []
                for s in surveys:
                    # overall quality stored in rating
                    if getter == 'overall':
                        vals.append(s.rating or 0)
                    else:
                        extra = s.get_additional_questions() or {}
                        v = extra.get(getter)
                        if isinstance(v, (int, float)):
                            vals.append(int(v))
                return (sum(vals) / len(vals)) if vals else 0.0
            survey_summary = type('Obj', (), dict(
                avg_overall=avg('overall'),
                avg_relevance=avg('content_relevance'),
                avg_confidence=avg('confidence_identify_attacks'),
                avg_usability=avg('ui_usability'),
                count=count
            ))
            latest_suggestions = [s for s in surveys if getattr(s, 'feedback_text', None)][:5]
        except Exception:
            survey_summary = None
            latest_suggestions = []

        return render_template('admin/dashboard.html',
                             total_users=total_users,
                             total_modules=total_modules,
                             total_assessments=total_assessments,
                             total_simulations=total_simulations,
                             recent_users=recent_users,
                             recent_assessments=recent_assessments,
                             recent_reflections=recent_reflections,
                             users_by_specialization=users_by_specialization,
                             users_by_year=users_by_year,
                             survey_summary=survey_summary,
                             latest_suggestions=latest_suggestions)
        
    except Exception as e:
        flash(f'Error loading admin dashboard: {e}', 'error')
        logger.error(f"Error loading admin dashboard: {e}")
        return redirect(url_for('dashboard'))

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """User management page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        users = User.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/users.html', users=users)
        
    except Exception as e:
        flash(f'Error loading users: {e}', 'error')
        logger.error(f"Error loading users: {e}")
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/<int:user_id>')
@login_required
@admin_required
def admin_user_detail(user_id):
    """User detail page"""
    try:
        user = User.get_by_id(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
        
        # Sync user progress counters with actual data
        user.sync_progress_counters()
        
        # Get user progress
        progress = UserProgress.get_user_progress(user_id)
        assessments = AssessmentResult.query.filter_by(user_id=user_id).all()
        simulations = SimulationResult.query.filter_by(user_id=user_id).all()
        
        return render_template('admin/user_detail.html',
                             user=user,
                             progress=progress,
                             assessments=assessments,
                             simulations=simulations)
        
    except Exception as e:
        flash(f'Error loading user details: {e}', 'error')
        logger.error(f"Error loading user details: {e}")
        return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    """Edit user information"""
    try:
        user = User.get_by_id(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
        
        if request.method == 'POST':
            # Update user information
            user.full_name = request.form.get('full_name', user.full_name)
            user.email = request.form.get('email', user.email)
            user.specialization = request.form.get('specialization', user.specialization)
            user.year_level = request.form.get('year_level', user.year_level)
            user.address = request.form.get('address', user.address)
            
            if user.save():
                flash('User updated successfully!', 'success')
                return redirect(url_for('admin_user_detail', user_id=user_id))
            else:
                flash('Error updating user.', 'error')
        
        return render_template('admin/edit_user.html', user=user)
        
    except Exception as e:
        flash(f'Error editing user: {e}', 'error')
        logger.error(f"Error editing user: {e}")
        return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    """Delete user"""
    try:
        user = User.get_by_id(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
        
        if user.username == 'administrator':
            flash('Cannot delete administrator account.', 'error')
            return redirect(url_for('admin_users'))
        
        if user.delete():
            flash('User deleted successfully!', 'success')
        else:
            flash('Error deleting user.', 'error')
        
        return redirect(url_for('admin_users'))
        
    except Exception as e:
        flash(f'Error deleting user: {e}', 'error')
        logger.error(f"Error deleting user: {e}")
        return redirect(url_for('admin_users'))

@app.route('/admin/modules')
@login_required
@admin_required
def admin_modules():
    """Module management page"""
    try:
        # Get all modules including Final Assessment
        modules = Module.query.filter(Module.id <= 6).order_by(Module.id).all()
        return render_template('admin/modules.html', modules=modules)
        
    except Exception as e:
        flash(f'Error loading modules: {e}', 'error')
        logger.error(f"Error loading modules: {e}")
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/analytics')
@login_required
@admin_required
def admin_analytics():
    """Analytics and reporting page"""
    try:
        # Get basic system statistics
        total_users = User.count()
        total_modules = Module.count()
        total_assessments = AssessmentResult.count()
        total_simulations = SimulationResult.count()
        
        # Create basic system stats
        system_stats = {
            'total_users': total_users,
            'total_modules': total_modules,
            'total_assessments': total_assessments,
            'total_simulations': total_simulations
        }
        
        # Create basic user performance data
        user_performance = {
            'completion_distribution': {
                'completed_all': 0,
                'completed_half': 0,
                'started': 0,
                'not_started': 0
            },
            'average_scores': {
                'knowledge_check': 0,
                'final_assessment': 0,
                'simulation': 0
            }
        }
        
        # Create basic module analytics
        module_analytics = {}
        
        return render_template('admin/analytics.html',
                             system_stats=system_stats,
                             user_performance=user_performance,
                             module_analytics=module_analytics)
        
    except Exception as e:
        flash(f'Error loading analytics: {e}', 'error')
        logger.error(f"Error loading analytics: {e}")
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/settings')
@login_required
@admin_required
def admin_settings():
    """System settings page"""
    try:
        return render_template('admin/settings.html')
        
    except Exception as e:
        flash(f'Error loading settings: {e}', 'error')
        logger.error(f"Error loading settings: {e}")
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/sync-module1-questions')
@login_required
@admin_required
def admin_sync_module1_questions():
    """Admin utility to replace Module 1 knowledge check questions with the latest set from learning_modules."""
    try:
        # from learning_modules.module1 import Module1Questions
        # Remove existing questions for module 1
        removed = KnowledgeCheckQuestion.query.filter_by(module_id=1).delete()
        db.session.commit()

        # Helper to normalize question dicts
        def normalize(q: dict, set_num: int) -> dict:
            data = {}
            # Map expected fields
            data['question_text'] = q.get('question_text') or q.get('question') or ''
            data['option_a'] = q.get('option_a', '')
            data['option_b'] = q.get('option_b', '')
            data['option_c'] = q.get('option_c', '')
            data['option_d'] = q.get('option_d', '')
            data['correct_answer'] = q.get('correct_answer', '')
            data['explanation'] = q.get('explanation', '')
            data['module_id'] = 1
            data['question_set'] = set_num
            return data

        # Insert set 1 - TEMPORARILY DISABLED
        # for q in Module1Questions.get_question_set_1():
        #     data = normalize(q, 1)
        #     db.session.add(KnowledgeCheckQuestion(**data))

        # Insert set 2 - TEMPORARILY DISABLED
        # for q in Module1Questions.get_question_set_2():
        #     data = normalize(q, 2)
        #     db.session.add(KnowledgeCheckQuestion(**data))

        db.session.commit()
        flash(f"Module 1 questions synchronized. Removed: {removed}", 'success')
        return redirect(url_for('admin_modules'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Sync Module 1 questions failed: {e}")
        flash(f"Error syncing Module 1 questions: {e}", 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/force-seed-module1')
@login_required
@admin_required
def admin_force_seed_module1():
    """Hard seed Module 1 questions with explicit field mapping."""
    try:
        # from learning_modules.module1 import Module1Questions
        KnowledgeCheckQuestion.query.filter_by(module_id=1).delete()
        db.session.commit()

        def to_row(q: dict, set_num: int) -> KnowledgeCheckQuestion:
            return KnowledgeCheckQuestion(
                question_text=q.get('question_text') or q.get('question') or '',
                option_a=q.get('option_a', ''),
                option_b=q.get('option_b', ''),
                option_c=q.get('option_c', ''),
                option_d=q.get('option_d', ''),
                correct_answer=q.get('correct_answer', ''),
                explanation=q.get('explanation', ''),
                module_id=1,
                question_set=set_num
            )

        rows = []
        # for q in Module1Questions.get_question_set_1():
        #     rows.append(to_row(q, 1))
        # for q in Module1Questions.get_question_set_2():
        #     rows.append(to_row(q, 2))
        for r in rows:
            db.session.add(r)
        db.session.commit()
        flash(f"Force-seeded Module 1 questions: {len(rows)}", 'success')
        return redirect(url_for('admin_modules'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Force seed Module 1 failed: {e}")
        flash(f"Error force-seeding Module 1: {e}", 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/seed-module1-kc')
@login_required
@admin_required
def admin_seed_module1_kc():
    """Seed Module 1 Knowledge Check questions from PDF in learning_modules/Documents/module1_KnowledgeCheck.pdf

    Parsing rules (best-effort):
    - Questions formatted with options A-D (e.g., 'A.', 'B.', 'C.', 'D.')
    - Correct answer indicated by a line starting with 'Answer:' or 'Correct:' followed by a letter a-d/A-D
    - Each question is saved as KnowledgeCheckQuestion; question_set alternates 1,2,1,2,... to support retakes
    """
    try:
        import os
        import re
        from data_models.content_models import KnowledgeCheckQuestion

        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'learning_modules', 'Documents', 'module1_KnowledgeCheck.pdf')
        if not os.path.exists(pdf_path):
            flash('module1_KnowledgeCheck.pdf not found in learning_modules/Documents', 'error')
            return redirect(url_for('admin_modules'))

        # Extract text from PDF using pdfplumber if available, else PyPDF2
        full_text = ''
        try:
            import pdfplumber  # type: ignore
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    full_text += '\n' + (page.extract_text() or '')
        except Exception:
            try:
                from PyPDF2 import PdfReader  # type: ignore
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    full_text += '\n' + (page.extract_text() or '')
            except Exception as pdf_e:
                logger.error(f"Failed to read PDF: {pdf_e}")
                flash('Failed to read PDF. Install pdfplumber or ensure PDF text is selectable.', 'error')
                return redirect(url_for('admin_modules'))

        # Normalize whitespace
        text = re.sub(r"\r", "\n", full_text)
        text = re.sub(r"\n+", "\n", text)

        # Split into question blocks heuristically
        # Accept patterns like '1.' or '1)' at the start of a line
        blocks = re.split(r"\n(?=\s*\d+\s*[\.)]\s)", text)
        parsed = []
        for block in blocks:
            b = block.strip()
            if not b:
                continue
            # Capture question line
            # Remove leading number prefix
            question_line = re.sub(r"^\d+\s*[\.)]\s*", "", b).strip()
            # Extract options
            opt_a = re.search(r"\n\s*A[\.)]\s*(.*)", b)
            opt_b = re.search(r"\n\s*B[\.)]\s*(.*)", b)
            opt_c = re.search(r"\n\s*C[\.)]\s*(.*)", b)
            opt_d = re.search(r"\n\s*D[\.)]\s*(.*)", b)
            # Extract answer and optional explanation
            ans = re.search(r"\n\s*(Answer|Correct)\s*[:\-]\s*([ABCDabcd])", b)
            expl = None
            expl_match = re.search(r"\n\s*(Explanation|Why)\s*[:\-]\s*(.*)", b)
            if expl_match:
                expl = expl_match.group(2).strip()

            if opt_a and opt_b and opt_c and opt_d and ans:
                parsed.append({
                    'question_text': question_line,
                    'option_a': opt_a.group(1).strip(),
                    'option_b': opt_b.group(1).strip(),
                    'option_c': opt_c.group(1).strip(),
                    'option_d': opt_d.group(1).strip(),
                    'correct_answer': ans.group(2).lower(),
                    'explanation': expl or ''
                })

        if not parsed:
            flash('No questions parsed from PDF. Please verify formatting (A-D options and Answer: X).', 'error')
            return redirect(url_for('admin_modules'))

        # Replace existing Module 1 questions
        removed = KnowledgeCheckQuestion.query.filter_by(module_id=1).delete()
        db.session.commit()

        # Insert, alternating question_set 1/2
        inserted = 0
        for idx, q in enumerate(parsed):
            row = KnowledgeCheckQuestion(
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                module_id=1,
                question_set=1 if (idx % 2 == 0) else 2
            )
            db.session.add(row)
            inserted += 1
        db.session.commit()

        flash(f"Module 1 Knowledge Check seeded from PDF. Removed: {removed}, Inserted: {inserted}", 'success')
        return redirect(url_for('admin_modules'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Seed Module 1 KC failed: {e}")
        flash(f"Error seeding Module 1 Knowledge Check: {e}", 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/seed-module1-kc-manual')
@login_required
@admin_required
def admin_seed_module1_kc_manual():
    """Seed Module 1 Knowledge Check with the provided curated questions (Lesson 1.1 and 1.2)."""
    try:
        from data_models.content_models import KnowledgeCheckQuestion

        questions = [
            {
                'question_text': 'According to Lesson 1.1, which of the following is the most accurate definition of social engineering?',
                'option_a': 'The use of complex code to bypass a digital firewall.',
                'option_b': 'The practice of analyzing social media to improve network security.',
                'option_c': 'The art of manipulating people into giving up confidential information by exploiting psychological tricks.',
                'option_d': 'The process of building better, more secure computer hardware.',
                'correct_answer': 'c',
                'explanation': "Social engineering is 'human hacking' — manipulating people using psychological tricks."
            },
            {
                'question_text': 'What is the primary way social engineering differs from a traditional technical hack?',
                'option_a': 'Social engineering is only used for pranks, while technical hacking is for serious crimes.',
                'option_b': 'Social engineering targets the human user to bypass security, while technical hacking targets vulnerabilities in software or systems.',
                'option_c': 'Social engineering requires advanced programming skills, while technical hacking does not.',
                'option_d': 'Social engineering can only be done over the phone, not through email.',
                'correct_answer': 'b',
                'explanation': 'Key difference: people vs. systems. Social engineering targets human behavior to bypass controls.'
            },
            {
                'question_text': "You receive an email 'URGENT: Your Student Portal Password Will Expire in 24 Hours!' from the 'Registrar's Office' with a link. This attack primarily uses which two principles?",
                'option_a': 'Liking and Social Proof',
                'option_b': 'Scarcity and Liking',
                'option_c': 'Authority and Urgency',
                'option_d': 'Scarcity and Authority',
                'correct_answer': 'c',
                'explanation': 'Impersonating a trusted department (Authority) and forcing quick action (Urgency).'
            },
            {
                'question_text': 'Based on the examples in the lessons (Bitcoin scam, GCash requests), what is a common motivation for social engineers?',
                'option_a': "To test a company's firewall for weaknesses.",
                'option_b': 'To make new friends and connections online.',
                'option_c': 'To gain access to information or resources for personal or financial benefit.',
                'option_d': 'To help users become more skeptical and informed.',
                'correct_answer': 'c',
                'explanation': 'Attackers aim for valuable gain: money, access, or sensitive data.'
            },
            {
                'question_text': 'A pop-up says: "FREE 1000 GEMS! Limited to the first 500 players!" This tactic relies on the principle of:',
                'option_a': 'Authority',
                'option_b': 'Liking',
                'option_c': 'Scarcity',
                'option_d': 'Social Proof',
                'correct_answer': 'c',
                'explanation': 'Creating fear of missing out (limited slots) is classic Scarcity.'
            },
            {
                'question_text': "You get a Messenger from a classmate: 'Urgent! My GCash is down, please send ₱500 to this number.' This primarily exploits:",
                'option_a': 'Authority',
                'option_b': 'Scarcity',
                'option_c': 'Liking',
                'option_d': 'Social Proof',
                'correct_answer': 'c',
                'explanation': 'It leverages a trusted relationship — the Liking principle.'
            },
            {
                'question_text': 'The lessons refer to social engineering as "human hacking" because it:',
                'option_a': 'Requires the hacker to be physically present.',
                'option_b': 'Can only be done by very friendly and popular people.',
                'option_c': "Targets people's natural tendencies and psychology instead of computer code.",
                'option_d': 'Is a legal method for testing security.',
                'correct_answer': 'c',
                'explanation': 'It exploits human psychology rather than code-level flaws.'
            },
            {
                'question_text': 'Which scenario describes a social engineering attack, as explained in the module?',
                'option_a': "A hacker exploits a website's code to access a database.",
                'option_b': 'A scammer pretends to be IT and convinces an employee to reveal a password.',
                'option_c': 'A script tries thousands of passwords on a login page.',
                'option_d': 'An admin installs a new firewall.',
                'correct_answer': 'b',
                'explanation': 'Only B manipulates a person into compromising security.'
            },
            {
                'question_text': 'A fake giveaway uses bots to add thousands of likes and comments saying "It works!" to convince users. This is an example of:',
                'option_a': 'Authority',
                'option_b': 'Social Proof',
                'option_c': 'Urgency',
                'option_d': 'Liking',
                'correct_answer': 'b',
                'explanation': 'Relying on the crowd’s behavior to influence decisions is Social Proof.'
            }
        ]

        # Replace existing Module 1 KC questions
        removed = KnowledgeCheckQuestion.query.filter_by(module_id=1).delete()
        db.session.commit()

        # Insert alternating sets 1/2
        for idx, q in enumerate(questions):
            row = KnowledgeCheckQuestion(
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation'],
                module_id=1,
                question_set=1 if (idx % 2 == 0) else 2
            )
            db.session.add(row)
        db.session.commit()

        flash(f"Module 1 KC seeded manually. Removed: {removed}, Inserted: {len(questions)}", 'success')
        return redirect(url_for('admin_modules'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manual seed Module 1 KC failed: {e}")
        flash(f"Error manual seeding Module 1 KC: {e}", 'error')
        return redirect(url_for('admin_modules'))

@app.route('/create-admin')
def create_admin():
    """Create admin user if it doesn't exist - DIRECT APPROACH"""
    try:
        with app.app_context():
            # Ensure database tables exist
            db.create_all()
            
            # Check if admin user already exists
            admin_user = User.query.filter_by(username='administrator').first()
            
            if admin_user:
                # Update existing admin user
                admin_user.email = 'admin@mmdc.edu.ph'
                admin_user.full_name = 'System Administrator'
                admin_user.specialization = 'Information Technology'
                admin_user.year_level = '4th Year'
                admin_user.set_password('Admin123!@#2025')
                admin_user.save()
                return f"✅ Admin user updated successfully<br>Username: administrator<br>Password: Admin123!@#2025<br>Email: admin@mmdc.edu.ph"
            else:
                # Create new admin user
                admin_data = {
                    'username': 'administrator',
                    'email': 'admin@mmdc.edu.ph',
                    'password': 'Admin123!@#2025',
                    'full_name': 'System Administrator',
                    'specialization': 'Information Technology',
                    'year_level': '4th Year'
                }
                
                user = user_service.create_user(admin_data)
                if user:
                    return f"✅ Admin user created successfully<br>Username: administrator<br>Password: Admin123!@#2025<br>Email: admin@mmdc.edu.ph"
                else:
                    return f"❌ Failed to create admin user"
                
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/create-admin-direct')
def create_admin_direct():
    """Create admin user using direct SQLAlchemy - BACKUP METHOD"""
    try:
        with app.app_context():
            # Ensure database tables exist
            db.create_all()
            
            # Check if admin user already exists
            admin_user = User.query.filter_by(username='administrator').first()
            
            if admin_user:
                # Update existing admin user
                admin_user.email = 'admin@mmdc.edu.ph'
                admin_user.full_name = 'System Administrator'
                admin_user.specialization = 'Information Technology'
                admin_user.year_level = '4th Year'
                admin_user.set_password('Admin123!@#2025')
                db.session.commit()
                return f"✅ Admin user updated successfully (Direct Method)<br>Username: administrator<br>Password: Admin123!@#2025<br>Email: admin@mmdc.edu.ph"
            else:
                # Create new admin user directly
                from werkzeug.security import generate_password_hash
                
                admin_user = User(
                    username='administrator',
                    email='admin@mmdc.edu.ph',
                    password_hash=generate_password_hash('Admin123!@#2025'),
                    full_name='System Administrator',
                    specialization='Information Technology',
                    year_level='4th Year'
                )
                
                db.session.add(admin_user)
                db.session.commit()
                return f"✅ Admin user created successfully (Direct Method)<br>Username: administrator<br>Password: Admin123!@#2025<br>Email: admin@mmdc.edu.ph"
                
    except Exception as e:
        return f"❌ Direct Method Error: {str(e)}"

@app.route('/admin/modules/<int:module_id>/edit')
@login_required
@admin_required
def admin_edit_module(module_id):
    """Edit module content page"""
    try:
        module = Module.get_by_id(module_id)
        if not module:
            flash('Module not found.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Get module content using ModuleManagerService
        from business_services.module_manager_service import ModuleManagerService
        module_manager = ModuleManagerService()
        
        # Get module content
        content = module_manager.get_module_content(module_id)
        questions = module_manager.get_knowledge_check_questions(module_id)
        
        # Ensure content is a dictionary
        if content is None:
            content = {
                'title': module.title,
                'description': module.description,
                'content': 'No content available',
                'learning_objectives': [],
                'estimated_time': 30,
                'difficulty_level': 'intermediate'
            }
        
        return render_template('admin/edit_module.html', 
                             module=module, 
                             content=content, 
                             questions=questions)
        
    except Exception as e:
        flash(f'Error loading module content: {e}', 'error')
        logger.error(f"Error loading module content: {e}")
        return redirect(url_for('admin_modules'))

@app.route('/admin/modules/<int:module_id>/update', methods=['POST'])
@login_required
@admin_required
def admin_update_module(module_id):
    """Update module content"""
    try:
        module = Module.get_by_id(module_id)
        if not module:
            flash('Module not found.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('admin_edit_module', module_id=module_id))
        
        # Update module basic info
        module.title = title
        module.description = description
        
        if module.save():
            flash('Module updated successfully!', 'success')
        else:
            flash('Error updating module.', 'error')
        
        return redirect(url_for('admin_edit_module', module_id=module_id))
        
    except Exception as e:
        flash(f'Error updating module: {e}', 'error')
        logger.error(f"Error updating module: {e}")
        return redirect(url_for('admin_modules'))


# =============================================================================
# 12. ASSESSMENT ROUTES
# =============================================================================

@app.route('/assessment/start')
@login_required
def start_new_assessment():
    """Start a new assessment attempt"""
    try:
        # Import here to avoid circular imports
        from data_models.assessment_models import AssessmentAttempt, AssessmentSession
        
        # Check if user can start a new attempt (exempt admin from limits)
        if not current_user.is_admin and not AssessmentAttempt.can_start_new_attempt(current_user.id):
            attempts = AssessmentAttempt.get_user_attempts(current_user.id)
            if len(attempts) >= 3:
                flash('You have reached the maximum number of attempts (3).', 'error')
                return redirect(url_for('final_assessment'))
            
            latest_attempt = attempts[0] if attempts else None
            if latest_attempt and not latest_attempt.is_eligible_for_retake():
                time_remaining = latest_attempt.completed_at + timedelta(hours=24) - datetime.utcnow()
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                flash(f'You must wait {hours}h {minutes}m before your next attempt.', 'error')
                return redirect(url_for('final_assessment'))
        
        # Create new attempt
        attempt_number = AssessmentAttempt.get_next_attempt_number(current_user.id)
        attempt = AssessmentAttempt(
            user_id=current_user.id,
            attempt_number=attempt_number
        )
        
        if not attempt.save():
            flash('Failed to create assessment attempt.', 'error')
            return redirect(url_for('final_assessment'))
        
        # Get random 25 questions from the pool
        all_questions = FinalAssessmentQuestion.query.all()
        if len(all_questions) < 25:
            flash('Not enough questions available for assessment.', 'error')
            return redirect(url_for('final_assessment'))
        
        # Shuffle and select 25 questions
        random_questions = random.sample(all_questions, 25)
        question_ids = [q.id for q in random_questions]
        
        # Set questions for this attempt
        attempt.set_questions_used(question_ids)
        attempt.save()
        
        # Create assessment session
        assessment_session = AssessmentSession.create_session(
            user_id=current_user.id,
            attempt_id=attempt.id,
            hours=2  # 2-hour time limit
        )
        
        if not assessment_session:
            flash('Failed to create assessment session.', 'error')
            return redirect(url_for('final_assessment'))
        
        # Store session token
        session['assessment_token'] = assessment_session.session_token
        
        return render_template('assessment/assessment.html', 
                             attempt=attempt, 
                             questions=random_questions,
                             session_token=assessment_session.session_token)
        
    except Exception as e:
        logger.error(f"Error starting assessment: {e}")
        flash('An error occurred while starting the assessment.', 'error')
        return redirect(url_for('final_assessment'))

@app.route('/assessment/submit', methods=['POST'])
@login_required
def submit_new_assessment():
    """Submit assessment answers"""
    try:
        # Import here to avoid circular imports
        from data_models.assessment_models import AssessmentAttempt, AssessmentSession
        
        session_token = request.form.get('session_token')
        if not session_token:
            flash('Invalid session.', 'error')
            return redirect(url_for('final_assessment'))
        
        # Get active session
        assessment_session = AssessmentSession.get_active_session(session_token)
        if not assessment_session:
            flash('Session expired or invalid.', 'error')
            return redirect(url_for('final_assessment'))
        
        # Get attempt
        attempt = AssessmentAttempt.get_by_id(assessment_session.attempt_id)
        if not attempt:
            flash('Assessment attempt not found.', 'error')
            return redirect(url_for('final_assessment'))
        
        # Collect answers
        answers = {}
        question_ids = attempt.get_questions_used()
        
        for question_id in question_ids:
            answer = request.form.get(f'question_{question_id}')
            if answer:
                answers[question_id] = answer
        
        # Set answers and calculate score
        attempt.set_answers(answers)
        score = attempt.calculate_score()
        attempt.completed_at = datetime.utcnow()
        attempt.save()
        
        # Invalidate session
        AssessmentSession.invalidate_session(session_token)
        session.pop('assessment_token', None)
        
        # Determine result message
        if attempt.passed:
            result_message = "Congratulations! You passed the assessment."
            result_type = "success"
        else:
            result_message = f"You scored {score:.1f}%. You need 80% to pass. You can retry in 24 hours."
            result_type = "warning"
        
        return render_template('assessment/result.html',
                             attempt=attempt,
                             score=score,
                             passed=attempt.passed,
                             result_message=result_message,
                             result_type=result_type)
        
    except Exception as e:
        logger.error(f"Error submitting assessment: {e}")
        flash('An error occurred while submitting the assessment.', 'error')
        return redirect(url_for('final_assessment'))

@app.route('/assessment/status')
@login_required
def new_assessment_status():
    """Get user's assessment status"""
    try:
        # Import here to avoid circular imports
        from data_models.assessment_models import AssessmentAttempt
        
        attempts = AssessmentAttempt.get_user_attempts(current_user.id)
        latest_attempt = attempts[0] if attempts else None
        
        can_retake = AssessmentAttempt.can_start_new_attempt(current_user.id)
        
        status = {
            'total_attempts': len(attempts),
            'max_attempts': 3,
            'can_retake': can_retake,
            'latest_score': latest_attempt.score if latest_attempt else None,
            'latest_passed': latest_attempt.passed if latest_attempt else False,
            'next_attempt_available': True
        }
        
        if latest_attempt and not can_retake:
            if len(attempts) >= 3:
                status['next_attempt_available'] = False
                status['reason'] = 'Maximum attempts reached'
            else:
                time_remaining = latest_attempt.completed_at + timedelta(hours=24) - datetime.utcnow()
                status['next_attempt_available'] = False
                status['reason'] = f'Wait {int(time_remaining.total_seconds() // 3600)}h {int((time_remaining.total_seconds() % 3600) // 60)}m'
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting assessment status: {e}")
        return jsonify({'error': 'Failed to get assessment status'}), 500

# =============================================================================
# 12. REFLECTION SUBMISSION ROUTE
# =============================================================================

@app.route('/submit_reflection', methods=['POST'])
@login_required
def submit_reflection():
    """Simple reflection submission endpoint"""
    try:
        data = request.get_json()
        reflection_text = data.get('reflection_text', '').strip()
        module_id = data.get('module_id', 1)
        
        if not reflection_text:
            return jsonify({'success': False, 'error': 'Reflection text is required'})
        
        # Create simple reflection record
        reflection = SimpleReflection(
            user_id=current_user.id,
            module_id=module_id,
            reflection_text=reflection_text
        )
        
        if reflection.save():
            logger.info(f"User {current_user.username} submitted reflection for module {module_id}")
            return jsonify({'success': True, 'message': 'Reflection submitted successfully!'})
        else:
            return jsonify({'success': False, 'error': 'Failed to save reflection'})
            
    except Exception as e:
        logger.error(f"Error submitting reflection: {e}")
        return jsonify({'success': False, 'error': 'An error occurred while submitting your reflection'})

@app.route('/api/module_reflections')
@login_required
def api_module_reflections():
    """Return latest public reflections for a module (max N)."""
    try:
        module_id = int(request.args.get('module_id', 0))
        limit = int(request.args.get('limit', 3))
        limit = max(1, min(limit, 20))

        if module_id <= 0:
            return jsonify({'reflections': []})

        q = SimpleReflection.query.filter_by(module_id=module_id).order_by(SimpleReflection.created_at.desc()).limit(limit)
        items = []
        for r in q.all():
            user = getattr(r, 'user', None)
            user_name = (getattr(user, 'full_name', None) or getattr(user, 'username', None) or 'Student') if user else 'Student'
            items.append({
                'user_name': user_name,
                'module_id': r.module_id,
                'reflection_text': r.reflection_text,
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M') if getattr(r, 'created_at', None) else ''
            })

        return jsonify({'reflections': items})
    except Exception as e:
        logger.error(f"Error fetching module reflections: {e}")
        return jsonify({'reflections': []})

# =============================================================================
# 13. APPLICATION ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    """
    Main application entry point.
    
    This section:
    - Initializes the application
    - Sets up logging
    - Configures the server
    - Starts the Flask development server
    
    For production deployment, use Gunicorn with the Procfile.
    """
    logger.info("[STARTUP] Initializing Social Engineering Awareness Program with OOP...")
    
    try:
        # Initialize database when app starts (not during import)
        with app.app_context():
            try:
                init_database()
                logger.info("[SUCCESS] Database initialized on startup")
            except Exception as e:
                logger.error(f"[ERROR] Database initialization on startup failed: {e}")
                # Continue anyway - the app might still work
        
        # Get configuration
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        # Log startup information
        logger.info(f"[SUCCESS] Application ready on port {port}")
        logger.info(f"[INFO] Debug mode: {debug}")
        logger.info(f"[INFO] Access the application at: http://localhost:{port}")
        logger.info(f"[INFO] Default admin credentials: {app.config.get('DEFAULT_ADMIN_USERNAME')} / {app.config.get('DEFAULT_ADMIN_PASSWORD')}")
        logger.info(f"[INFO] Health check available at: http://localhost:{port}/health")
        
        # Start the application
        app.run(debug=debug, host='0.0.0.0', port=port) 
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to start application: {e}")
        sys.exit(1)

# =============================================================================
# 13. DATABASE INITIALIZATION FOR PRODUCTION
# =============================================================================

# Simple database initialization that works with Flask 3.0
# This runs when the module is imported but after all functions are defined
try:
    with app.app_context():
        # Always try to create tables first, then check if data exists
        db.create_all()
        logger.info("[SUCCESS] Database tables created")
        
        # Only populate data if database is empty
        if Module.count() == 0:
            create_default_data()
            logger.info("[SUCCESS] Database initialized on import (production)")
        else:
            logger.info("[SUCCESS] Database already has data")
except Exception as e:
    logger.error(f"[ERROR] Production database init failed: {e}")
    # Continue anyway - the app will work and can be initialized via /init-db endpoint 
