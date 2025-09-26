"""
Configuration settings for Social Engineering Awareness Program
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me-in-production')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    # Database Configuration
    if os.environ.get('RENDER'):
        # Use PostgreSQL on Render for persistence
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            # Normalize scheme (Render sometimes provides postgres://)
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)

            # Ensure sslmode=require for managed Postgres
            if 'sslmode=' not in db_url:
                separator = '&' if '?' in db_url else '?'
                db_url = f"{db_url}{separator}sslmode=require"

            SQLALCHEMY_DATABASE_URI = db_url
        else:
            # Temporary fallback for testing - use SQLite in /tmp
            # WARNING: Data will be lost on restart without PostgreSQL
            SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/social_engineering_awareness.db'
    else:
        # Local development - use SQLite by default unless DATABASE_URL is set
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
            SQLALCHEMY_DATABASE_URI = db_url
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///social_engineering_awareness.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 10
    }
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.environ.get('RENDER', False)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = 'social_engineering_session'
    
    # Security Configuration
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SPECIAL = False
    
    # Assessment Configuration
    KNOWLEDGE_CHECK_PASSING_SCORE = 80  # Percentage
    FINAL_ASSESSMENT_PASSING_SCORE = 70  # Percentage
    MAX_ASSESSMENT_ATTEMPTS = 3
    ASSESSMENT_COOLDOWN_HOURS = 48
    
    # Module Configuration
    TOTAL_MODULES = 5
    MODULES_WITH_SIMULATIONS = [2, 3, 4, 5]  # Module IDs that have simulations
    
    # Simulation Configuration
    SIMULATION_TYPES = ['phishing', 'pretexting', 'baiting', 'quid_pro_quo']
    
    # Admin Configuration
    DEFAULT_ADMIN_USERNAME = 'administrator'
    DEFAULT_ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@mmdc.edu.ph')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin123!@#2025')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'app.log'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'static/profile_pictures'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Email Configuration (for password reset)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Application Information
    APP_NAME = 'Social Engineering Awareness Program'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Educational platform for social engineering awareness'
    ORGANIZATION = 'Mapúa Malayan Digital College (MMDC)'
    
    # Performance Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    TEMPLATES_AUTO_RELOAD = False
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains' if os.environ.get('RENDER') else None
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    LOG_LEVEL = 'DEBUG'
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    LOG_LEVEL = 'WARNING'
    
    # Enhanced production security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Production database settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 10,
        'echo': False
    }

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}
