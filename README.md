# 🛡️ Social Engineering Awareness Program

A **production-ready, enterprise-grade Flask application** that delivers comprehensive interactive learning on social engineering threats, defenses, and incident response. Built with modern software engineering practices, this platform provides a structured curriculum with knowledge checks, real-world simulations, advanced analytics, and professional certification.

**🌐 Live Demo**: [social-engineering-awareness.onrender.com](https://mmdcsea.onrender.com)

**📚 Repository**: [clarkorcullo/SocialEngineeringAwareness](https://github.com/clarkorcullo/SocialEngineeringAwareness)

---

## 🎯 Project Overview

This educational platform guides learners through **seven comprehensive modules** and a final assessment, enforcing strict completion rules and offering realistic practice via **four types of simulations** (Phishing, Pretexting, Baiting, Quid Pro Quo). The system tracks detailed progress, scores, time spent, and recent activity, supporting survey collection and certificate generation upon completion.

### 🏗️ Architecture Principles
- **Clean Architecture**: Separation of concerns via service layer (`business_services/`) and data models (`data_models/`)
- **Content-First Design**: Educational content is code-first and versioned in `learning_modules/`
- **OOP Patterns**: Simulations follow Base → Concrete OOP pattern in `simulations/`
- **Production Ready**: Enterprise-grade logging, error handling, and monitoring

---

## 🚀 Key Features

### 📚 **Comprehensive Learning Modules**
- **7 Progressive Modules**: From basic concepts to advanced incident response
- **Sequential Unlocking**: Each module requires previous completion
- **Knowledge Checks**: 5 questions per module with detailed feedback
- **Interactive Content**: Rich HTML content with practical examples

### 🎮 **Real-World Simulations**
- **4 Simulation Types**: Phishing, Pretexting, Baiting, Quid Pro Quo
- **OOP Design**: `BaseSimulation` + specific implementations
- **Real-time Feedback**: Red-flag explanations and learning points
- **Scenario-Based**: Authentic social engineering scenarios

### 📊 **Advanced Assessment System**
- **Module Knowledge Checks**: 5 questions/module, unlimited retakes
- **Final Assessment**: 25 questions, 3 retakes every 48 hours
- **Automatic Grading**: Percentage computation and attempts tracking
- **Progress Analytics**: Detailed completion metrics and time tracking

### 👤 **Professional User Management**
- **Secure Registration**: Comprehensive validation and security checks
- **Flask-Login Integration**: Robust authentication system
- **Profile Management**: Avatar uploads and detailed user profiles
- **Progress Tracking**: Consistent progress monitoring across all activities

### 📈 **Enterprise Analytics & Reporting**
- **Completion Metrics**: Rate, average scores, simulations completed
- **Time Analytics**: Detailed time spent tracking
- **Activity Feeds**: Recent activities and achievements
- **Certificate Generation**: Professional completion certificates

---

## 🏗️ Technology Stack

### **Backend Technologies**
- **Flask 2.3.3**: Modern Python web framework
- **SQLAlchemy 2.0.23**: Advanced ORM with type safety
- **Flask-Login 0.6.3**: Secure authentication system
- **Werkzeug 2.3.7**: WSGI utilities and security features

### **Frontend Technologies**
- **Bootstrap 5**: Modern, responsive UI framework
- **HTML5/CSS3**: Semantic markup and advanced styling
- **JavaScript**: Interactive functionality and dynamic content
- **Font Awesome**: Professional iconography

### **Architecture & Design**
- **Object-Oriented Programming**: Clean, maintainable code structure
- **Service Layer Pattern**: Business logic encapsulation
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Flexible application configuration

### **Production Features**
- **Gunicorn**: Production WSGI server
- **Comprehensive Logging**: File and console output
- **Health Monitoring**: `/health` endpoint for monitoring
- **Error Handling**: Professional error pages and logging

---

## 📁 Project Structure

```
CapstoneProject/
├── 🚀 Core Application
│   ├── app.py                          # Main Flask application (1,196 lines)
│   ├── config.py                       # Environment-based configuration
│   ├── manage.py                       # Database management utilities
│   ├── requirements.txt                # Python dependencies
│   ├── runtime.txt                     # Python 3.9.18 specification
│   ├── Procfile                        # Render deployment configuration
│   └── .gitignore                      # Git ignore rules
│
├── 🗄️ Data Layer
│   └── data_models/                    # Database models and ORM
│       ├── __init__.py                 # Model exports
│       ├── base_models.py              # Base classes and mixins
│       ├── user_models.py              # User and authentication models
│       ├── content_models.py           # Module and content models
│       └── progress_models.py          # Progress tracking models
│
├── ⚙️ Business Logic
│   └── business_services/              # Service layer architecture
│       ├── __init__.py                 # Service exports
│       ├── user_service.py             # User management (304 lines)
│       ├── module_service.py           # Module management (276 lines)
│       ├── assessment_service.py       # Assessment and grading (271 lines)
│       ├── simulation_service.py       # Simulation management (206 lines)
│       ├── progress_service.py         # Progress tracking (358 lines)
│       ├── analytics_service.py        # Analytics and reporting (424 lines)
│       └── module_manager_service.py   # Module coordination (348 lines)
│
├── 📚 Educational Content
│   └── learning_modules/               # Learning content and questions
│       ├── __init__.py                 # Content exports
│       ├── module1.py                  # Introduction to Social Engineering
│       ├── module2.py                  # Types of Social Engineering Attacks
│       ├── module3.py                  # Phishing Detection and Prevention
│       ├── module4.py                  # Password Security and Authentication
│       ├── module5.py                  # Social Media Security
│       ├── module6.py                  # Physical Security and Social Engineering
│       ├── module7.py                  # Incident Response and Reporting
│       └── final_assessment.py         # Final assessment content
│
├── 🎮 Interactive Simulations
│   └── simulations/                    # Simulation engine
│       ├── __init__.py                 # Simulation exports
│       ├── base_simulation.py          # Base simulation class
│       ├── phishing_simulation.py      # Phishing scenarios
│       ├── pretexting_simulation.py    # Pretexting scenarios
│       ├── baiting_simulation.py       # Baiting scenarios
│       └── quid_pro_quo_simulation.py  # Quid pro quo scenarios
│
├── 🛠️ Utilities
│   └── helper_utilities/               # Utility functions and helpers
│       ├── __init__.py                 # Utility exports
│       ├── constants.py                # Application constants (395 lines)
│       ├── formatters.py               # Data formatting utilities (311 lines)
│       └── validators.py               # Input validation utilities (269 lines)
│
├── 🎨 User Interface
│   ├── templates/                      # HTML templates (19 files)
│   │   ├── base.html                   # Base template with navigation
│   │   ├── index.html                  # Home page (617 lines)
│   │   ├── login.html                  # Login interface
│   │   ├── register.html               # Registration form (518 lines)
│   │   ├── dashboard.html              # User dashboard (434 lines)
│   │   ├── module.html                 # Module content (1,159 lines)
│   │   ├── assessment_simple.html      # Assessment interface
│   │   ├── simulation_simple.html      # Simulation interface
│   │   ├── final_assessment_simple.html # Final assessment
│   │   ├── survey.html                 # Feedback survey
│   │   ├── certificate.html            # Certificate generation
│   │   ├── profile.html                # User profile (348 lines)
│   │   ├── forgot_password.html        # Password reset
│   │   ├── reset_password.html         # Password reset confirmation
│   │   ├── 404.html                    # Error page
│   │   └── 500.html                    # Server error page
│   │
│   └── static/                         # Static assets
│       ├── MMDCLogo.png               # MMDC logo
│       ├── SEALogo.png                # Social Engineering Awareness logo
│       ├── Background.png             # Background image
│       └── profile_pictures/          # User profile pictures
│
└── 📄 Documentation
    ├── README.md                       # This comprehensive documentation
    └── LICENSE                         # MIT License
```

---

## 🎓 Learning Modules Overview

### **Module 1: Introduction to Social Engineering**
- **Content**: Basic concepts, psychology, and fundamental principles
- **Topics**: Why social engineering works, common targets, impacts
- **Assessment**: 5 knowledge check questions
- **Simulation**: None (foundational module)

### **Module 2: Types of Social Engineering Attacks**
- **Content**: Comprehensive attack type overview
- **Topics**: Phishing, pretexting, baiting, quid pro quo, tailgating
- **Assessment**: 5 knowledge check questions
- **Simulation**: Quid Pro Quo scenario

### **Module 3: Phishing Detection and Prevention**
- **Content**: Email and web-based phishing techniques
- **Topics**: Email phishing identification, website spoofing detection
- **Assessment**: 5 knowledge check questions
- **Simulation**: Phishing email scenario

### **Module 4: Password Security and Authentication**
- **Content**: Modern authentication security
- **Topics**: Strong password creation, MFA, security best practices
- **Assessment**: 5 knowledge check questions
- **Simulation**: Pretexting scenario

### **Module 5: Social Media Security**
- **Content**: Social media privacy and security
- **Topics**: Privacy settings, information sharing risks, attack vectors
- **Assessment**: 5 knowledge check questions
- **Simulation**: Baiting scenario

### **Module 6: Physical Security and Social Engineering**
- **Content**: Physical access control and environmental security
- **Topics**: Physical access control, in-person social engineering
- **Assessment**: 5 knowledge check questions
- **Simulation**: None (theoretical focus)

### **Module 7: Incident Response and Reporting**
- **Content**: Professional incident response procedures
- **Topics**: Incident detection, response procedures, reporting protocols
- **Assessment**: 5 knowledge check questions
- **Simulation**: None (procedural focus)

### **Final Assessment**
- **Content**: Comprehensive evaluation of all modules
- **Format**: 25 questions covering all topics
- **Requirements**: All modules must be completed
- **Attempts**: 3 attempts allowed every 48 hours

---

## ✅ Completion Rules & Access Control

### **Module Completion Requirements**
A module is considered **fully completed** when:
- ✅ **Knowledge Check Score** ≥ 80% (configurable)
- ✅ **Simulation Completed** (when module includes one - Modules 2-5)
- ✅ **Content Reviewed** (all sections accessed)

### **Progressive Unlocking System**
- 🔒 **Module 1**: Always accessible
- 🔒 **Modules 2-7**: Require previous module completion
- 🔒 **Final Assessment**: Requires all modules completed
- 🔒 **Certificate**: Requires final assessment passed + survey completed

### **Assessment Rules**
- 📝 **Knowledge Checks**: Unlimited retakes, 80% passing score
- 📝 **Final Assessment**: 3 attempts every 48 hours, 70% passing score
- 📝 **Simulations**: One attempt per simulation type
- 📝 **Progress Tracking**: Automatic saving and resume capability

---

## 🚀 Getting Started

### **Prerequisites**
- **Python 3.9+** (specified in runtime.txt)
- **pip** (Python package installer)
- **Git** (for version control)

### **Installation Steps**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/clarkorcullo/SocialEngineeringAwareness.git
   cd SocialEngineeringAwareness
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   - Open browser: `http://localhost:5000`
   - **Default Admin Credentials**:
     - Username: `administrator`
     - Password: `Admin123!@#2025`

### **Database Setup**
The application automatically:
- ✅ Creates database on first run
- ✅ Loads all educational content
- ✅ Creates default admin user
- ✅ Initializes all modules and questions

---

## 🔧 Configuration

### **Environment Variables**
```bash
# Essential Configuration
SECRET_KEY=your-secure-secret-key-here
FLASK_ENV=production
PORT=5000

# Admin Configuration
ADMIN_EMAIL=admin@mmdc.edu.ph
ADMIN_PASSWORD=Admin123!@#2025

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log

# Render Deployment
RENDER=true  # Automatically set by Render platform
```

### **Database Configuration**
- **Development**: SQLite database in `instance/` folder
- **Production**: SQLite on `/tmp/` (Render) or PostgreSQL
- **Testing**: In-memory SQLite database

### **Security Configuration**
- **Password Requirements**: 12+ characters, uppercase, lowercase, numbers
- **Session Security**: Secure cookies, HTTP-only, SameSite
- **CSRF Protection**: Built-in Flask-WTF protection
- **Input Validation**: Comprehensive validation on all inputs

---

## 🚀 Deployment

### **Render Deployment (Recommended)**
1. **Connect GitHub Repository** to Render
2. **Create Web Service** with Python environment
3. **Set Environment Variables**:
   ```bash
   SECRET_KEY=your-secure-secret-key
   FLASK_ENV=production
   ADMIN_EMAIL=your-admin-email
   ADMIN_PASSWORD=your-secure-password
   ```
4. **Deploy**: Automatic deployment from GitHub

### **Local Development**
```bash
# Development mode
export FLASK_ENV=development
python app.py

# Production mode
export FLASK_ENV=production
gunicorn app:app
```

### **Docker Deployment**
```dockerfile
FROM python:3.9.18-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app"]
```

---

## 📊 API Endpoints

### **Authentication Endpoints**
- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /logout` - User logout
- `GET /forgot_password` - Password reset request
- `POST /reset_password/<token>` - Password reset

### **Learning Endpoints**
- `GET /dashboard` - User dashboard with progress
- `GET /module/<id>` - Module content and progress
- `GET /assessment/<id>` - Module knowledge check
- `POST /submit_assessment/<id>` - Submit assessment answers
- `GET /final_assessment` - Final assessment access
- `POST /submit_final_assessment` - Submit final assessment

### **Simulation Endpoints**
- `GET /simulation/<type>` - Access simulation
- `POST /submit_simulation` - Submit simulation results
- `GET /simulation_result/<id>` - View simulation results

### **Progress & Profile Endpoints**
- `POST /update_progress` - Update module progress
- `GET /profile` - User profile page
- `POST /update_profile` - Update user profile
- `GET /certificate` - Generate completion certificate

### **System Endpoints**
- `GET /health` - Health check for monitoring
- `GET /survey` - Feedback survey
- `POST /submit_survey` - Submit survey responses

---

## 🧪 Testing & Quality Assurance

### **Code Quality**
- ✅ **Type Hints**: Full Python type annotation
- ✅ **Documentation**: Comprehensive docstrings
- ✅ **Error Handling**: Professional exception management
- ✅ **Logging**: Structured logging with multiple handlers

### **Security Testing**
- ✅ **Input Validation**: All user inputs validated
- ✅ **Authentication**: Secure login/logout system
- ✅ **Authorization**: Role-based access control
- ✅ **SQL Injection**: ORM prevents injection attacks
- ✅ **XSS Protection**: Template escaping enabled

### **Performance Testing**
- ✅ **Database Optimization**: Proper indexing and queries
- ✅ **Caching**: Template and query optimization
- ✅ **Memory Management**: Proper resource cleanup
- ✅ **Response Times**: Optimized routing and processing

---

## 📈 Analytics & Monitoring

### **Health Monitoring**
- **Health Check**: `/health` endpoint for uptime monitoring
- **Database Status**: Connection verification
- **Application Metrics**: Version and status information

### **User Analytics**
- **Progress Tracking**: Module completion rates
- **Assessment Scores**: Performance analytics
- **Time Analytics**: Learning time tracking
- **Activity Feeds**: Recent user activities

### **System Analytics**
- **Error Logging**: Comprehensive error tracking
- **Performance Metrics**: Response time monitoring
- **Usage Statistics**: User engagement analytics

---

## 🤝 Contributing

### **Development Setup**
1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Follow coding standards
4. **Test Thoroughly**: Ensure all functionality works
5. **Submit Pull Request**: Detailed description of changes

### **Coding Standards**
- **Python**: PEP 8 compliance
- **Type Hints**: Required for all functions
- **Documentation**: Docstrings for all classes/methods
- **Testing**: Unit tests for new features

### **Commit Guidelines**
- **Conventional Commits**: Use standard commit format
- **Descriptive Messages**: Clear commit descriptions
- **Atomic Commits**: One change per commit

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**MIT License Benefits**:
- ✅ **Commercial Use**: Can be used in commercial projects
- ✅ **Modification**: Can be modified and distributed
- ✅ **Distribution**: Can be distributed freely
- ✅ **Attribution**: Requires license and copyright notice

---

## 🆘 Support & Troubleshooting

### **Common Issues**

#### **Database Connection Issues**
```bash
# Reset database
python manage.py reset_database

# Create admin user
python manage.py create_admin username email password
```

#### **Module Loading Issues**
```bash
# Check module content
python manage.py list_modules

# Verify questions
python manage.py list_questions
```

#### **Deployment Issues**
```bash
# Check health endpoint
curl https://your-app.onrender.com/health

# Verify environment variables
echo $SECRET_KEY
echo $FLASK_ENV
```

### **Getting Help**
- 📖 **Documentation**: Check this README and code comments
- 🐛 **Issues**: Create detailed issue reports
- 💬 **Discussions**: Use GitHub discussions for questions
- 📧 **Contact**: Reach out to project maintainers

---

## 🎉 Acknowledgments

### **Educational Institutions**
- **Mapúa Malayan Digital College (MMDC)**: Academic support and guidance
- **Faculty Advisors**: Technical and educational oversight

### **Technology Stack**
- **Flask Community**: Excellent web framework
- **Bootstrap Team**: Beautiful UI components
- **Open Source Contributors**: Various libraries and tools

### **Security Community**
- **Cybersecurity Experts**: Content validation and review
- **Social Engineering Researchers**: Educational content accuracy
- **Security Awareness Advocates**: Best practices and guidelines

---

## 🔮 Future Enhancements

### **Planned Features**
- 🔄 **Multi-language Support**: Internationalization
- 📱 **Mobile App**: Native mobile application
- 🤖 **AI Integration**: Intelligent content recommendations
- 📊 **Advanced Analytics**: Machine learning insights
- 🔐 **Enhanced Security**: Additional authentication methods

### **Technical Improvements**
- 🚀 **Performance**: Caching and optimization
- 📈 **Scalability**: Microservices architecture
- 🔧 **DevOps**: CI/CD pipeline automation
- 🧪 **Testing**: Comprehensive test suite
- 📚 **Documentation**: API documentation with Swagger

---

## 📞 Contact Information

- **Repository**: [GitHub](https://github.com/clarkorcullo/SocialEngineeringAwareness)
- **Live Demo**: [Render Deployment](https://social-engineering-awareness.onrender.com/)
- **Issues**: [GitHub Issues](https://github.com/clarkorcullo/SocialEngineeringAwareness/issues)
- **Discussions**: [GitHub Discussions](https://github.com/clarkorcullo/SocialEngineeringAwareness/discussions)

---

## ⚠️ Important Notes

### **Educational Purpose**
This application is designed **exclusively for educational purposes** to raise awareness about social engineering attacks and prevention strategies. It should not be used for malicious purposes.

### **Security Disclaimer**
While this application demonstrates security concepts, it is not intended as a complete security solution. Always follow organizational security policies and consult with security professionals.

### **Data Privacy**
- User data is stored locally in SQLite database
- No personal information is shared with third parties
- Users can request data deletion
- Compliance with educational data privacy standards

---

**🎓 Built with ❤️ for Cybersecurity Education**

*Empowering the next generation of security-aware professionals through interactive learning and real-world simulations.*
