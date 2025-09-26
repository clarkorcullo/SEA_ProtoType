"""
Constants for the Social Engineering Awareness Program
"""

from enum import Enum

class AssessmentConstants:
    """Constants for assessment-related functionality"""
    
    # Passing thresholds
    PASSING_THRESHOLD = 70.0
    EXCELLENT_THRESHOLD = 90.0
    GOOD_THRESHOLD = 80.0
    AVERAGE_THRESHOLD = 70.0
    
    # Question counts
    DEFAULT_KNOWLEDGE_CHECK_QUESTIONS = 5
    DEFAULT_FINAL_ASSESSMENT_QUESTIONS = 10
    MAX_QUESTIONS_PER_ASSESSMENT = 20
    
    # Time limits (in minutes)
    KNOWLEDGE_CHECK_TIME_LIMIT = 15
    FINAL_ASSESSMENT_TIME_LIMIT = 30
    BASELINE_ASSESSMENT_TIME_LIMIT = 20
    
    # Assessment types
    BASELINE = "baseline"
    KNOWLEDGE_CHECK = "knowledge_check"
    FINAL_ASSESSMENT = "final_assessment"
    FOLLOW_UP = "follow_up"
    
    # Question types
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_IN_BLANK = "fill_in_blank"
    
    # Answer options
    VALID_ANSWER_OPTIONS = ['a', 'b', 'c', 'd']
    
    # Grading weights
    KNOWLEDGE_WEIGHT = 0.4
    ATTITUDE_WEIGHT = 0.3
    BEHAVIOR_WEIGHT = 0.3

class UserConstants:
    """Constants for user-related functionality"""
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    PASSWORD_REQUIREMENTS = {
        'uppercase': True,
        'lowercase': True,
        'numbers': True,
        'special_chars': False
    }
    
    # Username requirements
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 30
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]+$'
    
    # Email requirements
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Name requirements
    MIN_FULL_NAME_LENGTH = 2
    MAX_FULL_NAME_LENGTH = 100
    
    # Specializations
    VALID_SPECIALIZATIONS = [
        'Information Technology',
        'Computer Science',
        'Information Systems',
        'Cybersecurity',
        'Network Administration',
        'Software Engineering',
        'Data Science',
        'Other'
    ]
    
    # Year levels
    VALID_YEAR_LEVELS = [
        '1st Year',
        '2nd Year',
        '3rd Year',
        '4th Year',
        'Graduate',
        'Other'
    ]
    
    # Session timeout (in minutes)
    SESSION_TIMEOUT = 60
    
    # Password reset token expiry (in hours)
    PASSWORD_RESET_EXPIRY = 24
    
    # Maximum login attempts
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 15  # minutes

class ModuleConstants:
    """Constants for module-related functionality"""
    
    # Module status
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    
    # Module types
    THEORY = "theory"
    PRACTICAL = "practical"
    SIMULATION = "simulation"
    
    # Content types
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    
    # Module order limits
    MIN_MODULE_ORDER = 1
    MAX_MODULE_ORDER = 20
    
    # Content length limits
    MIN_CONTENT_LENGTH = 10
    MAX_CONTENT_LENGTH = 10000
    
    # Module name limits
    MIN_MODULE_NAME_LENGTH = 3
    MAX_MODULE_NAME_LENGTH = 200
    
    # Description limits
    MIN_DESCRIPTION_LENGTH = 10
    MAX_DESCRIPTION_LENGTH = 500
    
    # Time estimates (in minutes)
    DEFAULT_MODULE_TIME = 30
    MIN_MODULE_TIME = 5
    MAX_MODULE_TIME = 120

class SimulationConstants:
    """Constants for simulation-related functionality"""
    
    # Simulation types
    PHISHING = "phishing"
    PRETEXTING = "pretexting"
    BAITING = "baiting"
    QUID_PRO_QUO = "quid_pro_quo"
    
    # Simulation status
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    
    # Scoring
    MAX_SIMULATION_SCORE = 100
    PASSING_SIMULATION_SCORE = 70
    
    # Time limits (in minutes)
    DEFAULT_SIMULATION_TIME = 10
    MAX_SIMULATION_TIME = 30
    
    # Decision options
    VALID_DECISION_OPTIONS = ['a', 'b', 'c', 'd']
    
    # Scenario types
    EMAIL_SCENARIO = "email"
    PHONE_SCENARIO = "phone"
    IN_PERSON_SCENARIO = "in_person"
    SOCIAL_MEDIA_SCENARIO = "social_media"

class ProgressConstants:
    """Constants for progress tracking"""
    
    # Progress status
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    
    # Time tracking
    MIN_TIME_SPENT = 0
    MAX_TIME_SPENT = 1440  # 24 hours in minutes
    
    # Attempt limits
    MAX_ATTEMPTS_PER_MODULE = 10
    MAX_ATTEMPTS_PER_ASSESSMENT = 5
    
    # Completion requirements
    MIN_SCORE_TO_COMPLETE = 70
    MIN_TIME_TO_COMPLETE = 1  # minutes
    
    # Achievement thresholds
    FIRST_MODULE_ACHIEVEMENT = 1
    HALFWAY_ACHIEVEMENT = 4
    ALL_MODULES_ACHIEVEMENT = 5
    PERFECT_SCORE_ACHIEVEMENT = 100
    SPEED_LEARNER_THRESHOLD = 30  # minutes

class FeedbackConstants:
    """Constants for feedback and surveys"""
    
    # Rating scale
    MIN_RATING = 1
    MAX_RATING = 5
    
    # Difficulty levels
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    
    # Feedback types
    MODULE_FEEDBACK = "module"
    SYSTEM_FEEDBACK = "system"
    GENERAL_FEEDBACK = "general"
    
    # Text limits
    MAX_FEEDBACK_TEXT_LENGTH = 1000
    MIN_FEEDBACK_TEXT_LENGTH = 1
    
    # Required fields
    REQUIRED_FEEDBACK_FIELDS = ['rating']
    OPTIONAL_FEEDBACK_FIELDS = ['feedback_text', 'difficulty_level']

class SecurityConstants:
    """Constants for security-related functionality"""
    
    # Password reset
    PASSWORD_RESET_TOKEN_LENGTH = 32
    PASSWORD_RESET_EXPIRY_HOURS = 24
    
    # Session security
    SESSION_SECURE = True
    SESSION_HTTPONLY = True
    SESSION_SAMESITE = 'Lax'
    
    # CSRF protection
    CSRF_ENABLED = True
    CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 3600  # 1 hour
    
    # Input sanitization
    ALLOWED_HTML_TAGS = ['b', 'i', 'u', 'em', 'strong']
    MAX_INPUT_LENGTH = 1000
    
    # File upload
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_FILE_TYPES = ['jpg', 'jpeg', 'png', 'gif']
    UPLOAD_FOLDER = 'static/profile_pictures'

class DatabaseConstants:
    """Constants for database operations"""
    
    # Connection settings
    MAX_CONNECTIONS = 10
    CONNECTION_TIMEOUT = 30
    QUERY_TIMEOUT = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    MIN_PAGE_SIZE = 1
    
    # Cache settings
    CACHE_TIMEOUT = 300  # 5 minutes
    MAX_CACHE_SIZE = 1000
    
    # Backup settings
    BACKUP_RETENTION_DAYS = 30
    AUTO_BACKUP_ENABLED = True
    BACKUP_INTERVAL_HOURS = 24

class NotificationConstants:
    """Constants for notifications"""
    
    # Notification types
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    
    # Notification channels
    EMAIL = "email"
    IN_APP = "in_app"
    SMS = "sms"
    
    # Notification priorities
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    
    # Notification expiry (in days)
    NOTIFICATION_EXPIRY_DAYS = 30
    
    # Maximum notifications per user
    MAX_NOTIFICATIONS_PER_USER = 100

class AnalyticsConstants:
    """Constants for analytics and reporting"""
    
    # Time periods
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    
    # Chart types
    LINE_CHART = "line"
    BAR_CHART = "bar"
    PIE_CHART = "pie"
    DONUT_CHART = "donut"
    
    # Data aggregation
    SUM = "sum"
    AVERAGE = "average"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    
    # Export formats
    CSV = "csv"
    JSON = "json"
    PDF = "pdf"
    EXCEL = "excel"
    
    # Report types
    USER_PROGRESS_REPORT = "user_progress"
    MODULE_PERFORMANCE_REPORT = "module_performance"
    ASSESSMENT_ANALYSIS_REPORT = "assessment_analysis"
    SYSTEM_OVERVIEW_REPORT = "system_overview"

class ErrorConstants:
    """Constants for error handling"""
    
    # Error types
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    NOT_FOUND_ERROR = "not_found_error"
    SERVER_ERROR = "server_error"
    DATABASE_ERROR = "database_error"
    
    # Error codes
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    
    # Error messages
    DEFAULT_ERROR_MESSAGE = "An unexpected error occurred"
    VALIDATION_ERROR_MESSAGE = "Invalid input data"
    AUTHENTICATION_ERROR_MESSAGE = "Authentication required"
    AUTHORIZATION_ERROR_MESSAGE = "Access denied"
    NOT_FOUND_ERROR_MESSAGE = "Resource not found"
    
    # Log levels
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class FileConstants:
    """Constants for file operations"""
    
    # File size limits
    MAX_PROFILE_PICTURE_SIZE = 2 * 1024 * 1024  # 2MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Allowed file extensions
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']
    
    # File storage paths
    PROFILE_PICTURES_PATH = 'static/profile_pictures'
    DOCUMENTS_PATH = 'static/documents'
    TEMP_PATH = 'temp'
    
    # File naming
    MAX_FILENAME_LENGTH = 255
    FILENAME_PATTERN = r'^[a-zA-Z0-9._-]+$'
    
    # Backup settings
    BACKUP_PATH = 'backups'
    MAX_BACKUP_FILES = 10

