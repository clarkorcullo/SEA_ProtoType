# 📁 Project Structure Guide

## 🏗️ **SOCIAL ENGINEERING AWARENESS PROGRAM**

This document provides a comprehensive overview of the project structure, making it easy to understand, navigate, and edit the codebase.

---

## 📂 **Root Directory Structure**

```
CapstoneProject/
├── 🚀 CORE APPLICATION FILES
│   ├── app.py                    # Main Flask application (1,208 lines)
│   ├── config.py                 # Environment-based configuration
│   ├── manage.py                 # Database and system management utilities
│   ├── requirements.txt          # Python dependencies
│   ├── runtime.txt               # Python version specification
│   └── Procfile                  # Render deployment configuration
│
├── 📚 EDUCATIONAL CONTENT
│   └── learning_modules/         # Learning content and assessments
│       ├── __init__.py           # Module exports and initialization
│       ├── module1.py            # Introduction to Social Engineering
│       ├── module2.py            # Types of Social Engineering Attacks
│       ├── module3.py            # Phishing Detection and Prevention
│       ├── module4.py            # Password Security and Authentication
│       ├── module5.py            # Social Media Security
│       ├── module6.py            # Physical Security and Social Engineering
│       ├── module7.py            # Incident Response and Reporting
│       └── final_assessment.py   # Final assessment content
│
├── 🎮 INTERACTIVE SIMULATIONS
│   └── simulations/              # Simulation engine
│       ├── __init__.py           # Simulation exports
│       ├── base_simulation.py    # Base simulation class (OOP pattern)
│       ├── phishing_simulation.py      # Phishing scenarios
│       ├── pretexting_simulation.py    # Pretexting scenarios
│       ├── baiting_simulation.py       # Baiting scenarios
│       └── quid_pro_quo_simulation.py  # Quid pro quo scenarios
│
├── 🗄️ DATA LAYER
│   └── data_models/              # Database models and ORM
│       ├── __init__.py           # Model exports
│       ├── base_models.py        # Base classes and mixins
│       ├── user_models.py        # User and authentication models
│       ├── content_models.py     # Module and content models
│       └── progress_models.py    # Progress tracking models
│
├── ⚙️ BUSINESS LOGIC
│   └── business_services/        # Service layer architecture
│       ├── __init__.py           # Service exports
│       ├── user_service.py       # User management (304 lines)
│       ├── module_service.py     # Module management (276 lines)
│       ├── assessment_service.py # Assessment and grading (271 lines)
│       ├── simulation_service.py # Simulation management (206 lines)
│       ├── progress_service.py   # Progress tracking (358 lines)
│       ├── analytics_service.py  # Analytics and reporting (424 lines)
│       └── module_manager_service.py # Module coordination (348 lines)
│
├── 🛠️ UTILITIES
│   └── helper_utilities/         # Utility functions and helpers
│       ├── __init__.py           # Utility exports
│       ├── constants.py          # Application constants (395 lines)
│       ├── formatters.py         # Data formatting utilities (311 lines)
│       └── validators.py         # Input validation utilities (269 lines)
│
├── 🎨 USER INTERFACE
│   ├── templates/                # HTML templates (19 files)
│   │   ├── base.html             # Base template with navigation
│   │   ├── index.html            # Home page (617 lines)
│   │   ├── login.html            # Login interface
│   │   ├── register.html         # Registration form (518 lines)
│   │   ├── dashboard.html        # User dashboard (434 lines)
│   │   ├── module.html           # Module content (1,159 lines)
│   │   ├── assessment_simple.html      # Assessment interface
│   │   ├── simulation_simple.html      # Simulation interface
│   │   ├── final_assessment_simple.html # Final assessment
│   │   ├── survey.html           # Feedback survey
│   │   ├── certificate.html      # Certificate generation
│   │   ├── profile.html          # User profile (348 lines)
│   │   ├── forgot_password.html  # Password reset
│   │   ├── reset_password.html   # Password reset confirmation
│   │   ├── 404.html              # Error page
│   │   └── 500.html              # Server error page
│   │
│   └── static/                   # Static assets
│       ├── MMDCLogo.png         # MMDC logo
│       ├── SEALogo.png          # Social Engineering Awareness logo
│       ├── Background.png       # Background image
│       └── profile_pictures/    # User profile pictures
│
├── 📄 DOCUMENTATION
│   ├── README.md                 # Comprehensive project documentation
│   ├── PROJECT_STRUCTURE.md      # This file - project organization guide
│   └── LICENSE                   # MIT License
│
└── 🔧 DEVELOPMENT FILES
    ├── .gitignore                # Git ignore rules
    ├── app.log                   # Application logs
    └── instance/                 # Database and instance files
        └── social_engineering_awareness.db
```

---

## 🎯 **File Purpose and Organization**

### **🚀 Core Application Files**

| File | Purpose | Key Features |
|------|---------|--------------|
| **`app.py`** | Main Flask application | Routes, middleware, error handling |
| **`config.py`** | Environment configuration | Database, security, deployment settings |
| **`manage.py`** | Management utilities | Database operations, admin tasks |
| **`requirements.txt`** | Dependencies | Python packages and versions |
| **`runtime.txt`** | Python version | Specifies Python 3.9.18 |
| **`Procfile`** | Deployment config | Render deployment settings |

### **📚 Educational Content (`learning_modules/`)**

Each module file contains:
- **Content Structure**: HTML content with cybersecurity information
- **Question Sets**: Multiple-choice questions for assessments
- **Learning Objectives**: Clear goals for each module
- **Progressive Difficulty**: From basic to advanced concepts

**Module Progression:**
1. **Module 1**: What is Social Engineering
2. **Module 2**: Phishing: The Digital Net
3. **Module 3**: Fortifying Your Accounts
4. **Module 4**: Immediate Action After a Suspected Attack
5. **Module 5**: The Evolving Threat Landscape
6. **Final Assessment**: Comprehensive evaluation

### **🎮 Interactive Simulations (`simulations/`)**

**OOP Design Pattern:**
- **`base_simulation.py`**: Abstract base class with common functionality
- **Specific Simulations**: Each inherits from base class
- **Scenario-Based**: Real-world social engineering scenarios
- **Interactive Feedback**: Immediate learning feedback

**Simulation Types:**
- **Phishing**: Email and web-based attacks
- **Pretexting**: Impersonation scenarios
- **Baiting**: Physical device attacks
- **Quid Pro Quo**: Exchange-based attacks

### **🗄️ Data Layer (`data_models/`)**

**Database Architecture:**
- **`base_models.py`**: Common functionality and mixins
- **`user_models.py`**: User authentication and profiles
- **`content_models.py`**: Modules and educational content
- **`progress_models.py`**: Progress tracking and analytics

**Key Models:**
- **User**: Authentication, profiles, progress
- **Module**: Educational content and structure
- **Assessment**: Questions, answers, scoring
- **Progress**: User completion tracking
- **Simulation**: Interactive scenario results

### **⚙️ Business Logic (`business_services/`)**

**Service Layer Pattern:**
- **Separation of Concerns**: Business logic separated from routes
- **Reusability**: Services can be used across different routes
- **Testability**: Easy to unit test business logic
- **Maintainability**: Clear responsibility boundaries

**Service Responsibilities:**
- **UserService**: Registration, authentication, profile management
- **ModuleService**: Content delivery and module management
- **AssessmentService**: Question generation and grading
- **SimulationService**: Scenario management and scoring
- **ProgressService**: Progress tracking and analytics
- **AnalyticsService**: Reporting and statistics
- **ModuleManagerService**: Module coordination and access control

### **🛠️ Utilities (`helper_utilities/`)**

**Utility Functions:**
- **`constants.py`**: Application-wide constants and settings
- **`formatters.py`**: Data formatting and presentation
- **`validators.py`**: Input validation and security checks

**Common Utilities:**
- **Data Validation**: Email, password, input validation
- **Formatting**: Date, score, text formatting
- **Constants**: Configuration values and settings

### **🎨 User Interface (`templates/` & `static/`)**

**Template Structure:**
- **`base.html`**: Common layout and navigation
- **Page Templates**: Specific functionality pages
- **Error Pages**: 404 and 500 error handling
- **Responsive Design**: Bootstrap 5 framework

**Static Assets:**
- **Images**: Logos, backgrounds, profile pictures
- **CSS/JS**: Styling and interactive functionality
- **Fonts**: Typography and iconography

---

## 🔧 **Development Workflow**

### **📝 Adding New Features**

1. **Content Changes**:
   - Edit files in `learning_modules/` for educational content
   - Modify `simulations/` for new interactive scenarios
   - Update templates in `templates/` for UI changes

2. **Business Logic**:
   - Add new services in `business_services/`
   - Extend models in `data_models/` if needed
   - Update routes in `app.py`

3. **Configuration**:
   - Modify `config.py` for new settings
   - Update `requirements.txt` for new dependencies

### **🐛 Debugging and Maintenance**

1. **Logs**: Check `app.log` for application events
2. **Database**: Use `manage.py` for database operations
3. **Health Check**: Visit `/health` endpoint for system status
4. **Error Pages**: Check `templates/404.html` and `templates/500.html`

### **🚀 Deployment**

1. **Local Development**: `python app.py`
2. **Production**: Configure environment variables
3. **Render Deployment**: Automatic from GitHub
4. **Health Monitoring**: `/health` endpoint

---

## 📊 **Code Organization Principles**

### **🎯 Clean Architecture**
- **Separation of Concerns**: Each layer has specific responsibilities
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Single Responsibility**: Each class/module has one reason to change

### **🔄 Design Patterns**
- **Service Layer**: Business logic encapsulation
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Object creation and configuration
- **Observer Pattern**: Event handling and notifications

### **📈 Scalability**
- **Modular Design**: Easy to add new features
- **Configuration-Driven**: Environment-based settings
- **Database Abstraction**: ORM for database independence
- **Caching Ready**: Optimized for performance

---

## 🎓 **Educational Content Structure**

### **Module Content Format**
```python
class ModuleContent:
    @staticmethod
    def get_content():
        return {
            'title': 'Module Title',
            'description': 'Module description',
            'content': 'HTML content with cybersecurity information',
            'objectives': ['Learning objective 1', 'Learning objective 2'],
            'key_points': ['Key point 1', 'Key point 2']
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

### **Simulation Structure**
```python
class BaseSimulation:
    def __init__(self):
        self.scenarios = []
        self.current_scenario = 0
    
    def get_scenario(self, scenario_id):
        # Return specific scenario data
        pass
    
    def evaluate_response(self, response):
        # Evaluate user response and provide feedback
        pass
```

---

## 🔍 **Quick Reference**

### **Common File Locations**
- **Main App**: `app.py`
- **Configuration**: `config.py`
- **Database Models**: `data_models/`
- **Business Logic**: `business_services/`
- **Educational Content**: `learning_modules/`
- **Simulations**: `simulations/`
- **Templates**: `templates/`
- **Static Files**: `static/`

### **Key Routes**
- **Home**: `/`
- **Login**: `/login`
- **Dashboard**: `/dashboard`
- **Module**: `/module/<id>`
- **Assessment**: `/assessment/<id>`
- **Simulation**: `/simulation/<type>`
- **Health Check**: `/health`

### **Management Commands**
```bash
# Reset database
python manage.py reset_database

# Create admin user
python manage.py create_admin username email password

# List users
python manage.py list_users

# List modules
python manage.py list_modules

# Backup database
python manage.py backup_database
```

---

## 🎉 **Getting Started**

1. **Understand the Structure**: Review this document
2. **Set Up Environment**: Install dependencies from `requirements.txt`
3. **Run Application**: Execute `python app.py`
4. **Access Application**: Visit `http://localhost:5000`
5. **Explore Features**: Navigate through modules and simulations
6. **Make Changes**: Edit files based on your needs
7. **Test Thoroughly**: Ensure all functionality works
8. **Deploy**: Push to GitHub for automatic deployment

---

**📚 This structure makes the project easy to understand, navigate, and modify while maintaining clean architecture and best practices.**
