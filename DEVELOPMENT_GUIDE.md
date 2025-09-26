# 🛠️ DEVELOPMENT GUIDE

## 🎯 **SOCIAL ENGINEERING AWARENESS PROGRAM**

This comprehensive guide provides everything you need to understand, modify, and extend the Social Engineering Awareness Program.

---

## 📚 **QUICK START**

### **1. Understanding the Project**
- **Purpose**: Educational platform for social engineering awareness
- **Architecture**: Clean Architecture with Service Layer Pattern
- **Technology**: Flask, SQLAlchemy, Bootstrap 5
- **Deployment**: Render (cloud platform)

### **2. Key Files to Know**
```
📁 Core Files:
├── app.py              # Main application (1,208 lines)
├── config.py           # Configuration management
├── manage.py           # Database utilities
└── requirements.txt    # Dependencies

📁 Content Files:
├── learning_modules/   # Educational content
├── simulations/        # Interactive scenarios
└── templates/          # User interface

📁 Logic Files:
├── data_models/        # Database models
├── business_services/  # Business logic
└── helper_utilities/   # Utility functions
```

---

## 🔧 **DEVELOPMENT WORKFLOW**

### **Making Changes**

#### **1. Content Changes (Educational Material)**
```bash
# Edit learning content
📁 learning_modules/module1.py
📁 learning_modules/module2.py
# ... etc

# Edit simulation scenarios
📁 simulations/phishing_simulation.py
📁 simulations/pretexting_simulation.py
# ... etc
```

**Content Structure:**
```python
class ModuleContent:
    @staticmethod
    def get_content():
        return {
            'title': 'Module Title',
            'description': 'Module description',
            'content': 'HTML content with cybersecurity information'
        }
    
    @staticmethod
    def get_question_set_1():
        return [
            {
                'question': 'Question text?',
                'option_a': 'Option A',
                'option_b': 'Option B',
                'option_c': 'Option C',
                'option_d': 'Option D',
                'correct_answer': 'a',
                'explanation': 'Why this answer is correct'
            }
        ]
```

#### **2. Business Logic Changes**
```bash
# Edit business services
📁 business_services/user_service.py
📁 business_services/assessment_service.py
📁 business_services/simulation_service.py
# ... etc
```

**Service Pattern:**
```python
class UserService:
    @staticmethod
    def create_user(user_data):
        """Create a new user with validation"""
        # Validation logic
        # Business rules
        # Database operations
        pass
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user credentials"""
        # Authentication logic
        pass
```

#### **3. Database Model Changes**
```bash
# Edit data models
📁 data_models/user_models.py
📁 data_models/content_models.py
📁 data_models/progress_models.py
# ... etc
```

**Model Pattern:**
```python
class User(BaseModel):
    """User model for authentication and profiles"""
    
    # Database fields
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Methods
    def check_password(self, password):
        """Verify password"""
        pass
    
    @classmethod
    def get_by_username(cls, username):
        """Get user by username"""
        pass
```

#### **4. User Interface Changes**
```bash
# Edit templates
📁 templates/base.html
📁 templates/dashboard.html
📁 templates/module.html
# ... etc

# Edit static assets
📁 static/
├── CSS files
├── JavaScript files
└── Images
```

**Template Structure:**
```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<!-- Page content here -->
<div class="container">
    <h1>{{ title }}</h1>
    <!-- Content -->
</div>
{% endblock %}
```

---

## 🎨 **DESIGN PATTERNS**

### **1. Service Layer Pattern**
```python
# Business logic in services, not routes
@app.route('/dashboard')
@login_required
def dashboard():
    # Route only handles HTTP concerns
    user_stats = user_service.get_user_statistics(current_user.id)
    return render_template('dashboard.html', stats=user_stats)

# Business logic in service
class UserService:
    @staticmethod
    def get_user_statistics(user_id):
        # Complex business logic here
        return statistics
```

### **2. Repository Pattern**
```python
# Data access through models
class User(BaseModel):
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
```

### **3. Factory Pattern**
```python
# Configuration management
def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app
```

---

## 📝 **ADDING NEW FEATURES**

### **1. Adding a New Module**

#### **Step 1: Create Content**
```python
# learning_modules/module8.py
class Module8Content:
    @staticmethod
    def get_content():
        return {
            'title': 'Advanced Social Engineering',
            'description': 'Advanced techniques and countermeasures',
            'content': '<h1>Advanced Content</h1><p>...</p>'
        }
    
    @staticmethod
    def get_question_set_1():
        return [
            {
                'question': 'What is the most advanced social engineering technique?',
                'option_a': 'Phishing',
                'option_b': 'Pretexting',
                'option_c': 'Advanced Persistent Threats',
                'option_d': 'Baiting',
                'correct_answer': 'c',
                'explanation': 'APTs are the most sophisticated form of social engineering.'
            }
        ]

class Module8Questions:
    @staticmethod
    def get_question_set_1():
        return Module8Content.get_question_set_1()
```

#### **Step 2: Update Database**
```python
# The module will be automatically created on next startup
# Or use manage.py to create it manually
```

#### **Step 3: Update Configuration**
```python
# config.py
class Config:
    TOTAL_MODULES = 8  # Update from 7 to 8
    MODULES_WITH_SIMULATIONS = [2, 3, 4, 5, 8]  # Add 8 if it has simulation
```

### **2. Adding a New Simulation**

#### **Step 1: Create Simulation Class**
```python
# simulations/advanced_simulation.py
from .base_simulation import BaseSimulation

class AdvancedSimulation(BaseSimulation):
    def __init__(self):
        super().__init__()
        self.simulation_type = 'advanced'
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self):
        return [
            {
                'id': 1,
                'title': 'Advanced Phishing Scenario',
                'description': 'Complex phishing attack scenario',
                'content': 'You receive an email from...',
                'options': ['Click the link', 'Delete the email', 'Forward to IT'],
                'correct_answer': 1,
                'explanation': 'Deleting suspicious emails is the safest action.'
            }
        ]
    
    def evaluate_response(self, scenario_id, response):
        """Evaluate user response and provide feedback"""
        scenario = self.get_scenario(scenario_id)
        is_correct = response == scenario['correct_answer']
        
        return {
            'correct': is_correct,
            'explanation': scenario['explanation'],
            'score': 100 if is_correct else 0
        }
```

#### **Step 2: Update Simulation Service**
```python
# business_services/simulation_service.py
from simulations.advanced_simulation import AdvancedSimulation

class SimulationService:
    def get_simulation_data(self, simulation_type):
        if simulation_type == 'advanced':
            return AdvancedSimulation().get_scenarios()
        # ... existing code
```

### **3. Adding a New Route**

#### **Step 1: Add Route to app.py**
```python
@app.route('/new_feature')
@login_required
def new_feature():
    """
    New feature route - brief description.
    
    Features:
    - Feature 1
    - Feature 2
    
    Returns:
        str: Rendered template
    """
    try:
        # Get data from service
        data = some_service.get_data()
        
        return render_template('new_feature.html', data=data)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        logger.error(f"Error in new_feature: {e}")
        return redirect(url_for('dashboard'))
```

#### **Step 2: Create Template**
```html
<!-- templates/new_feature.html -->
{% extends "base.html" %}

{% block title %}New Feature{% endblock %}

{% block content %}
<div class="container">
    <h1>New Feature</h1>
    <!-- Content here -->
</div>
{% endblock %}
```

#### **Step 3: Add Navigation**
```html
<!-- templates/base.html -->
<nav>
    <!-- Add navigation link -->
    <a href="{{ url_for('new_feature') }}">New Feature</a>
</nav>
```

---

## 🔍 **DEBUGGING GUIDE**

### **1. Common Issues**

#### **Database Issues**
```bash
# Reset database
python manage.py reset_database

# Check database status
python manage.py list_modules
python manage.py list_users
```

#### **Import Errors**
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### **Template Errors**
```bash
# Check template syntax
# Look for missing {% endblock %} or {{ }}
# Check for undefined variables
```

### **2. Logging and Debugging**

#### **Check Application Logs**
```bash
# View recent logs
tail -f app.log

# Search for errors
grep "ERROR" app.log
```

#### **Health Check**
```bash
# Check application health
curl http://localhost:5000/health
```

#### **Database Debugging**
```python
# In Python console
from app import app, db
with app.app_context():
    # Check database connection
    db.session.execute('SELECT 1')
    
    # Check specific models
    from data_models import User
    users = User.query.all()
    print(f"Found {len(users)} users")
```

### **3. Performance Issues**

#### **Database Queries**
```python
# Enable SQL query logging
app.config['SQLALCHEMY_ECHO'] = True

# Check for N+1 queries
# Use eager loading where appropriate
users = User.query.options(db.joinedload('progress')).all()
```

#### **Memory Issues**
```python
# Check memory usage
import psutil
print(psutil.Process().memory_info().rss / 1024 / 1024)  # MB
```

---

## 🚀 **DEPLOYMENT GUIDE**

### **1. Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access at http://localhost:5000
```

### **2. Production Deployment**

#### **Environment Variables**
```bash
# Required
SECRET_KEY=your-secure-secret-key
FLASK_ENV=production

# Optional
ADMIN_EMAIL=admin@domain.com
ADMIN_PASSWORD=secure-password
LOG_LEVEL=INFO
```

#### **Render Deployment**
1. Connect GitHub repository to Render
2. Set environment variables
3. Deploy automatically

#### **Health Monitoring**
```bash
# Check application health
curl https://your-app.onrender.com/health

# Expected response:
{
    "status": "healthy",
    "database": "connected",
    "version": "1.0.0"
}
```

---

## 📊 **TESTING STRATEGY**

### **1. Manual Testing Checklist**

#### **Authentication**
- [ ] User registration
- [ ] User login/logout
- [ ] Password validation
- [ ] Session management

#### **Learning Modules**
- [ ] Module access control
- [ ] Content display
- [ ] Progress tracking
- [ ] Module completion

#### **Assessments**
- [ ] Question display
- [ ] Answer submission
- [ ] Score calculation
- [ ] Result display

#### **Simulations**
- [ ] Scenario display
- [ ] Response evaluation
- [ ] Feedback provision
- [ ] Score tracking

### **2. Automated Testing (Future)**

#### **Unit Tests**
```python
# tests/test_user_service.py
import unittest
from business_services.user_service import UserService

class TestUserService(unittest.TestCase):
    def test_create_user(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        user = UserService.create_user(user_data)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
```

#### **Integration Tests**
```python
# tests/test_app.py
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
```

---

## 🔧 **MAINTENANCE TASKS**

### **1. Regular Maintenance**

#### **Weekly Tasks**
- [ ] Review application logs
- [ ] Check health endpoint
- [ ] Monitor error rates
- [ ] Update dependencies

#### **Monthly Tasks**
- [ ] Database backup
- [ ] Performance review
- [ ] Security audit
- [ ] Content updates

#### **Quarterly Tasks**
- [ ] Major dependency updates
- [ ] Architecture review
- [ ] User feedback analysis
- [ ] Feature planning

### **2. Performance Optimization**

#### **Database Optimization**
```sql
-- Add indexes for frequently queried fields
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_progress_user_module ON user_progress(user_id, module_id);
```

#### **Caching Strategy**
```python
# Add caching for frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_module_content(module_id):
    return Module.get_by_id(module_id)
```

---

## 📚 **RESOURCES AND REFERENCES**

### **1. Documentation**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

### **2. Best Practices**
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/2.0.x/patterns/)
- [Security Best Practices](https://owasp.org/www-project-top-ten/)

### **3. Tools and Utilities**
- [Python Debugger (pdb)](https://docs.python.org/3/library/pdb.html)
- [Flask Debug Toolbar](https://flask-debugtoolbar.readthedocs.io/)
- [SQLAlchemy Query Profiler](https://github.com/sqlalchemy/sqlalchemy-utils)

---

## 🎯 **QUICK REFERENCE**

### **Common Commands**
```bash
# Start application
python app.py

# Database operations
python manage.py reset_database
python manage.py create_admin username email password

# Check health
curl http://localhost:5000/health

# View logs
tail -f app.log
```

### **File Locations**
```
📁 Main App: app.py
📁 Config: config.py
📁 Models: data_models/
📁 Services: business_services/
📁 Content: learning_modules/
📁 UI: templates/
📁 Assets: static/
```

### **Key Routes**
```
🏠 Home: /
🔐 Login: /login
📊 Dashboard: /dashboard
📚 Module: /module/<id>
📝 Assessment: /assessment/<id>
🎮 Simulation: /simulation/<type>
👤 Profile: /profile
🔧 Health: /health
```

---

**🎓 This development guide provides everything you need to work effectively with the Social Engineering Awareness Program. Use it as your reference for all development tasks!**
