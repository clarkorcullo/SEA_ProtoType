"""
Security middleware for the Social Engineering Awareness Program
Implements comprehensive security measures including CSRF protection,
rate limiting, input sanitization, and security headers.
"""

import os
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session, g, abort, make_response
from werkzeug.exceptions import TooManyRequests
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """Comprehensive security middleware for the application"""
    
    def __init__(self, app=None):
        self.app = app
        self.rate_limit_storage = {}
        self.failed_attempts = {}
        self.csrf_tokens = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security middleware with Flask app"""
        self.app = app
        
        # Register security decorators
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Register error handlers
        app.errorhandler(429)(self.rate_limit_handler)
        app.errorhandler(403)(self.csrf_error_handler)
        
        logger.info("Security middleware initialized")
    
    def before_request(self):
        """Security checks before each request"""
        # Rate limiting
        if not self.check_rate_limit():
            abort(429)
        
        # CSRF protection for state-changing requests
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if not self.verify_csrf_token():
                abort(403)
        
        # Security headers
        self.add_security_headers()
        
        # Input sanitization
        self.sanitize_inputs()
    
    def after_request(self, response):
        """Add security headers after request processing"""
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # HSTS for production
        if os.environ.get('RENDER'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    def check_rate_limit(self):
        """Check if request is within rate limits"""
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean old entries
        self.rate_limit_storage = {
            k: v for k, v in self.rate_limit_storage.items() 
            if current_time - v['last_request'] < 3600  # 1 hour window
        }
        
        # Check rate limit
        if client_ip in self.rate_limit_storage:
            if self.rate_limit_storage[client_ip]['count'] >= 100:  # 100 requests per hour
                return False
            self.rate_limit_storage[client_ip]['count'] += 1
        else:
            self.rate_limit_storage[client_ip] = {
                'count': 1,
                'last_request': current_time
            }
        
        return True
    
    def verify_csrf_token(self):
        """Verify CSRF token for state-changing requests"""
        # Skip CSRF for API endpoints that use proper authentication
        if request.path.startswith('/api/'):
            return True
        
        # Get token from form or header
        token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
        
        if not token:
            logger.warning(f"Missing CSRF token for {request.method} {request.path}")
            return False
        
        # Verify token
        if token in self.csrf_tokens:
            token_data = self.csrf_tokens[token]
            if datetime.now() < token_data['expires']:
                return True
            else:
                # Remove expired token
                del self.csrf_tokens[token]
        
        logger.warning(f"Invalid CSRF token for {request.method} {request.path}")
        return False
    
    def generate_csrf_token(self):
        """Generate a new CSRF token"""
        token = secrets.token_urlsafe(32)
        self.csrf_tokens[token] = {
            'expires': datetime.now() + timedelta(hours=1)
        }
        return token
    
    def add_security_headers(self):
        """Add security headers to request context"""
        g.security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-XSS-Protection': '1; mode=block'
        }
    
    def sanitize_inputs(self):
        """Sanitize user inputs to prevent XSS"""
        if request.method in ['POST', 'PUT', 'PATCH']:
            for key, value in request.form.items():
                if isinstance(value, str):
                    # Basic XSS prevention
                    sanitized = value.replace('<script', '&lt;script')
                    sanitized = sanitized.replace('</script>', '&lt;/script&gt;')
                    sanitized = sanitized.replace('javascript:', '')
                    request.form[key] = sanitized
    
    def rate_limit_handler(self, error):
        """Handle rate limit exceeded"""
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    def csrf_error_handler(self, error):
        """Handle CSRF token errors"""
        return jsonify({
            'error': 'CSRF token missing or invalid',
            'message': 'Security token validation failed.'
        }), 403

# Security decorators
def rate_limit(max_requests=10, window=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Simple in-memory rate limiting
            key = f"{client_ip}:{f.__name__}"
            if not hasattr(g, 'rate_limits'):
                g.rate_limits = {}
            
            if key in g.rate_limits:
                if current_time - g.rate_limits[key]['last_request'] < window:
                    if g.rate_limits[key]['count'] >= max_requests:
                        abort(429)
                    g.rate_limits[key]['count'] += 1
                else:
                    g.rate_limits[key] = {'count': 1, 'last_request': current_time}
            else:
                g.rate_limits[key] = {'count': 1, 'last_request': current_time}
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_csrf(f):
    """Require CSRF token for state-changing operations"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            if not token:
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def brute_force_protection(max_attempts=5, lockout_duration=900):
    """Brute force protection decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Check if IP is locked out
            if client_ip in g.failed_attempts:
                if current_time - g.failed_attempts[client_ip]['last_attempt'] < lockout_duration:
                    if g.failed_attempts[client_ip]['count'] >= max_attempts:
                        logger.warning(f"Brute force attempt blocked from {client_ip}")
                        abort(429)
            
            try:
                result = f(*args, **kwargs)
                # Reset failed attempts on successful authentication
                if client_ip in g.failed_attempts:
                    del g.failed_attempts[client_ip]
                return result
            except Exception as e:
                # Track failed attempts
                if not hasattr(g, 'failed_attempts'):
                    g.failed_attempts = {}
                
                if client_ip not in g.failed_attempts:
                    g.failed_attempts[client_ip] = {'count': 0, 'last_attempt': 0}
                
                g.failed_attempts[client_ip]['count'] += 1
                g.failed_attempts[client_ip]['last_attempt'] = current_time
                
                raise e
        
        return decorated_function
    return decorator

def input_validation(required_fields=None, max_length=None):
    """Input validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in ['POST', 'PUT', 'PATCH']:
                # Check required fields
                if required_fields:
                    for field in required_fields:
                        if field not in request.form and field not in request.json:
                            abort(400)
                
                # Check field lengths
                if max_length:
                    for key, value in request.form.items():
                        if isinstance(value, str) and len(value) > max_length:
                            abort(400)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Security utilities
def generate_secure_filename(filename):
    """Generate a secure filename to prevent path traversal"""
    import uuid
    import os
    
    # Get file extension
    _, ext = os.path.splitext(filename)
    
    # Generate secure filename
    secure_name = f"{uuid.uuid4().hex}{ext}"
    
    return secure_name

def validate_file_upload(file, allowed_extensions=None, max_size=None):
    """Validate file upload for security"""
    if not file:
        return False, "No file provided"
    
    # Check file size
    if max_size and file.content_length > max_size:
        return False, "File too large"
    
    # Check file extension
    if allowed_extensions:
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            return False, "File type not allowed"
    
    return True, "Valid file"

def log_security_event(event_type, details, user_id=None, ip_address=None):
    """Log security events for monitoring"""
    logger.warning(f"SECURITY_EVENT: {event_type} - {details} - User: {user_id} - IP: {ip_address or request.remote_addr}")

# Initialize security middleware
security = SecurityMiddleware()
