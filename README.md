## Social Engineering Awareness Program (SEAP)

SEAP is a friendly learning web app that helps students and staff spot scams, respond quickly during incidents, and build safe online habits. It uses short lessons, simple visuals, quick quizzes, reflections, and a final assessment.

- Live site: `https://mmdcsea.onrender.com`
- Repo: `https://github.com/clarkorcullo/SEA_ProtoType`

---

### What you can do
- Learn through 5 modules with videos, images, and examples
- Take a short “Knowledge Check” per module (via Start Knowledge Check button)
- Submit Reflections and read the latest 3 from others per module
- Take a 25‑question Final Assessment (80% to pass)
- Admins can view recent users, assessments, reflections, and simple analytics

---

### Modules
1) Module 1: Social Engineering (basics)
2) Module 2: Phishing — Spot the Scams
3) Module 3: Proactive Defender
4) Module 4: Immediate Action After a Suspected Attack
5) Module 5: The Evolving Threat Landscape
6) Final Assessment (25 questions)

Each module may include: lessons, a Reflection form, and a Knowledge Check button. Some modules also include simulations inside the module page.

---

### Key rules
- Knowledge Checks: short quizzes per module, pass at 80%
- Final Assessment: 25 questions, pass at 80%
- Reflections: latest 3 shown on each module page; Admin sees latest 5 across all modules
- Certificate generation: requires passing the Final Assessment and completing the Satisfaction Survey. Non-admin users must have a complete full name in Profile (first name + last name) before generating the certificate.

---

### How to run locally
1) Install Python 3.11+
2) Install dependencies:
   - `pip install -r requirements.txt`
3) Start the app:
   - `python app.py`
4) Open: `http://localhost:5000`

Local data: `instance/social_engineering_awareness.db` (SQLite)

---

### Deployment (Render)
- Connect the GitHub repo to Render and create a Web Service
- Uses included `Procfile` and `runtime.txt`
- Auto‑deploys when you push to `main`
- Health check: visit `/health` (shows status, DB, and app version)

Logging
- `app.log` rotates daily and keeps only the last 3 days

---

### 🛠️ Technology Stack

**Backend:**
- **Flask 3.0.0** - Web framework with security middleware
- **SQLAlchemy 2.0.36** - ORM with PostgreSQL/SQLite support
- **Flask-Login 0.6.3** - User authentication and session management
- **Flask-WTF 1.2.1** - CSRF protection and form handling
- **Werkzeug 3.0.1** - WSGI utilities and security features

**Security Libraries:**
- **Flask-Limiter 3.5.0** - Rate limiting and DDoS protection
- **Flask-Talisman 1.1.0** - Security headers and HTTPS enforcement
- **cryptography 41.0.7** - Cryptographic operations
- **bcrypt 4.1.2** - Password hashing

**Database:**
- **PostgreSQL** (Production) - Primary database with SSL
- **SQLite** (Development) - Local development database
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

**Deployment:**
- **Render.com** - Cloud hosting platform
- **Gunicorn 21.2.0** - WSGI HTTP server
- **Python 3.11+** - Runtime environment

**Frontend:**
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icon library
- **JavaScript ES6** - Interactive functionality
- **HTML5/CSS3** - Modern web standards

### Configuration
Environment variables (optional):
- `APP_VERSION` — shown in `/health` and Admin → System Settings (e.g., 1.1.0)
- `DATABASE_URL` — use Postgres in production; falls back to SQLite if not set
- `LOG_LEVEL` — default INFO
 
Certificate requirements policy
- Non-admins must complete their Profile full name (e.g., "Juan Dela Cruz"). The certificate route validates this and redirects to Profile if missing.
- Admins bypass this requirement for QA/testing.

Where to change the version
- Set `APP_VERSION` in your environment for deployment
- It is also displayed in Admin → System Settings; the code reads the value from the environment when available

---

### Admin overview
- User Dashboard → “Professional Review & Validation” links to the validator PDF
- Card limits and scrolling:
  - User Dashboard → Recent Activity: shows up to 3; scrolls if more
  - Admin Dashboard → Recent Assessments: shows up to 5; scrolls
  - Admin Dashboard → Recent Users: shows up to 5; scrolls
  - Admin Dashboard → Users Module Reflections: shows up to 5; scrolls (title stays fixed)
  - Module 6 → Certificate drawer: the yellow "Generate Certificate" button navigates to `/certificate` (server enforces eligibility and full-name policy).

---

### Assets
- Images and PDFs live in `learning_modules/Documents` and `learning_modules/Visual_Aid`
- Served via `/learning_assets/<path>` (e.g., the validator certification PDF)

---

### Troubleshooting
- “HTTP 503” on Render: usually a restart during deploy; wait a bit and refresh
- Missing images: confirm path under `/learning_assets/...` or `/static/...`
- Final Assessment count: should be exactly 25 questions; refresh after deploy

---

### 🔒 Security Features

**Enterprise-Grade Security Implementation:**
- ✅ **CSRF Protection** - All state-changing requests protected
- ✅ **Rate Limiting** - 100 requests per hour per IP
- ✅ **Brute Force Protection** - Account lockout after 5 failed attempts
- ✅ **Input Validation** - XSS and injection prevention
- ✅ **Secure File Upload** - Path traversal prevention, file type validation
- ✅ **Security Headers** - XSS protection, clickjacking prevention
- ✅ **Session Security** - Secure cookies, timeout enforcement
- ✅ **Password Security** - 12+ character requirements, 90-day expiration
- ✅ **Security Logging** - Comprehensive audit trail
- ✅ **OWASP Top 10** - All vulnerabilities addressed

**Security Score: 100/100** ✅

### Credits
Content validated by **Miss Thea Patrice Tajonera**, **SANS GIAC GCFA**, from **ANZ**.

Making our digital community safer, one learner at a time.


---

### Developer reference (deeper details)

- Routes (in `app.py`)
  - `/dashboard`: builds module cards, completion counts, recent activity
  - `/module/<id>`: reconciles status to Completed at ≥80%, renders `templates/module.html`
  - `/assessment/<id>`: loads questions (retake set logic: alternates set 1/2), auto‑seeds modules 4–5 if missing
  - `/submit_assessment/<id>`: grades, stores `AssessmentResult`, updates `UserProgress`
  - `/final_assessment` and `/final_assessment_questions`: selects exactly 25 questions
  - `/api/module_reflections`: returns last reflections for a module (used by UI cards)
  - `/learning_assets/<path>`: securely serves assets from `learning_modules/Documents` and `learning_modules/Visual_Aid`
  - Error handlers: custom 404 and 500 pages with logging

- Progress logic (in `data_models/progress_models.py`)
  - `UserProgress.update_score(percentage)`: if not completed and score ≥80, mark completed; never downgrade
  - `UserProgress.complete_progress(score)`: force mark completed and set timestamp

- Admin dashboard cards (`templates/admin/dashboard.html`)
  - Recent Assessments, Recent Users (max 5, scroll)
  - Users Module Reflections (max 5, scroll; fixed title)

- Learner dashboard card rules (`templates/dashboard.html`)
  - Status badge shows: Completed if module ID in `completed_module_ids`, else Current if accessible, else Locked
  - Recent Activity (UI): shows assessment, simulation, completion, and survey events (capped and scrollable)

- Module page shell (`templates/module.html`)
  - Shows Estimated Time, Difficulty, Interactive label, and a colored status badge (`completed` / `in-progress` / `not-started`)
  - Includes per‑module script via `{% include 'modules/moduleX.html' %}`

- Per‑module content files (`templates/modules/moduleX.html`)
  - Attach to drawer items by IDs and inject HTML on `DOMContentLoaded`
  - Images use absolute URLs built from `window.location.origin + '/learning_assets/…'`
  - Reflections: simple form POST, client‑side validation; latest 3 displayed
  - Knowledge Check: shows rules + “Start Knowledge Check” button linking to `/assessment/<id>`

- Logging
  - `TimedRotatingFileHandler`: rotates `app.log` nightly; keeps last 3 days
  - Level controlled by `LOG_LEVEL` (default INFO)

- Versioning
  - `/health` includes `{ "version": APP_VERSION }`
  - Set `APP_VERSION` in environment to change version shown in `/health` and Admin → System Settings


---

### Project structure (what each folder/file is for)

```text
CapstoneProject_ProtType_Backup/
├─ 🐍 CORE APPLICATION FILES
│  ├─ app.py                      # Main Flask application with all routes, middleware, and business logic
│  ├─ config.py                   # Application configuration (environment variables, security settings, database)
│  ├─ manage.py                   # Database management utilities and admin creation scripts
│  ├─ check_db.py                 # Database connection and health check utilities
│  ├─ check_modules_json.py       # Content validation for modules.json file
│  └─ migrate_production_database.py # Production database migration scripts
│
├─ 📦 DEPENDENCIES & DEPLOYMENT
│  ├─ requirements.txt            # Python package dependencies with security libraries
│  ├─ runtime.txt                 # Python version specification for Render deployment
│  ├─ Procfile                    # Gunicorn start command for Render deployment
│  └─ .venv/                      # Virtual environment directory (local development)
│
├─ 🗄️ DATABASE & DATA
│  ├─ instance/
│  │  └─ social_engineering_awareness.db # SQLite database (local development)
│  ├─ social_engineering_awareness.db   # SQLite database (production backup)
│  ├─ production_migration.sql          # SQL migration scripts for production
│  └─ content_seed/
│     └─ modules.json                   # Module metadata, descriptions, and content structure
│
├─ 🎨 FRONTEND TEMPLATES
│  ├─ templates/
│  │  ├─ base.html                    # Global layout template with header, footer, navigation
│  │  ├─ index.html                   # Landing page template
│  │  ├─ login.html                   # User authentication login form
│  │  ├─ register.html                # User registration form
│  │  ├─ dashboard.html               # Main user dashboard with progress tracking
│  │  ├─ profile.html                 # User profile management page
│  │  ├─ module.html                  # Individual module page template
│  │  ├─ certificate.html             # Certificate generation and display
│  │  ├─ forgot_password.html         # Password reset request form
│  │  ├─ reset_password.html          # Password reset form with token validation
│  │  ├─ survey.html                  # User feedback survey form
│  │  ├─ assessment.html              # Knowledge check assessment interface
│  │  ├─ assessment_result.html       # Assessment results display
│  │  ├─ assessment_simple.html       # Simplified assessment interface
│  │  ├─ final_assessment_questions.html # Final assessment question display
│  │  ├─ final_assessment_result.html    # Final assessment results
│  │  ├─ final_assessment_simple.html    # Simplified final assessment
│  │  ├─ simulation_simple.html         # Simulation interface
│  │  ├─ 404.html                      # Custom 404 error page
│  │  ├─ 500.html                      # Custom 500 error page
│  │  ├─ admin/                        # Admin dashboard templates
│  │  │  ├─ dashboard.html             # Admin main dashboard
│  │  │  ├─ users.html                 # User management interface
│  │  │  ├─ user_detail.html           # Individual user details and editing
│  │  │  ├─ edit_user.html             # User profile editing form
│  │  │  ├─ modules.html               # Module management interface
│  │  │  ├─ edit_module.html           # Module content editing
│  │  │  ├─ analytics.html             # Analytics and reporting dashboard
│  │  │  └─ settings.html              # System settings and configuration
│  │  ├─ assessment/                   # Assessment-related templates
│  │  │  ├─ assessment.html             # Assessment interface
│  │  │  └─ result.html                # Assessment results display
│  │  └─ modules/                      # Module-specific content templates
│  │     ├─ module1.html               # Module 1: Social Engineering basics
│  │     ├─ module1_drawer.html        # Module 1 drawer content
│  │     ├─ module2.html               # Module 2: Phishing detection
│  │     ├─ module3.html               # Module 3: Proactive defense
│  │     ├─ module4.html               # Module 4: Incident response
│  │     └─ module5.html               # Module 5: Evolving threats
│
├─ 🏗️ DATA MODELS & DATABASE
│  ├─ data_models/
│  │  ├─ __init__.py                   # Package initialization
│  │  ├─ base_models.py                # Base model classes and mixins
│  │  ├─ user_models.py                # User authentication and profile models
│  │  ├─ content_models.py             # Module and content management models
│  │  ├─ progress_models.py             # User progress and assessment tracking
│  │  └─ assessment_models.py           # Assessment and quiz models
│
├─ 🔧 BUSINESS LOGIC & SERVICES
│  ├─ business_services/
│  │  ├─ __init__.py                   # Package initialization
│  │  ├─ user_service.py               # User management and authentication logic
│  │  ├─ module_service.py             # Module content and progress logic
│  │  ├─ assessment_service.py         # Assessment creation and grading logic
│  │  ├─ analytics_service.py          # Analytics and reporting logic
│  │  ├─ progress_service.py          # Progress tracking and completion logic
│  │  └─ simulation_service.py         # Simulation and interactive content logic
│
├─ 🛠️ HELPER UTILITIES
│  ├─ helper_utilities/
│  │  ├─ __init__.py                   # Package initialization
│  │  ├─ constants.py                  # Application constants and configuration
│  │  ├─ database_persistence.py       # Database backup and restore utilities
│  │  ├─ formatters.py                 # Data formatting and display utilities
│  │  └─ validators.py                 # Input validation and sanitization
│
├─ 🎓 LEARNING CONTENT & ASSETS
│  ├─ learning_modules/
│  │  ├─ __init__.py                   # Package initialization
│  │  ├─ assessment/                   # Assessment content and questions
│  │  │  ├─ __init__.py                # Package initialization
│  │  │  └─ final_assessment_questions.py # Final assessment question bank
│  │  ├─ Documents/                    # Learning materials and documents
│  │  │  ├─ CertRibbon.png            # Certificate ribbon image
│  │  │  ├─ CertTemplate.png           # Certificate template
│  │  │  ├─ ClarosSign.png             # Digital signature image
│  │  │  ├─ finalAssessmentQuestioner.pdf # Final assessment PDF
│  │  │  ├─ KeyRisksofOversharing.png # Educational infographic
│  │  │  ├─ KimSignature.png           # Signature image
│  │  │  ├─ Lesson11.png               # Lesson 1 visual aid
│  │  │  ├─ Lesson21.png               # Lesson 2 visual aid
│  │  │  ├─ Lesson31StrongPassword.png # Password security visual
│  │  │  ├─ Lesson32SocialMediaInformationSharingSmarts.png # Social media security
│  │  │  ├─ lesson33TheVerificationToolkit.png # Verification toolkit
│  │  │  ├─ Lesson33VerifyingOnlineCommunications.png # Online verification
│  │  │  ├─ Lesson41.png               # Lesson 4 visual aid
│  │  │  ├─ Lesson42.png               # Lesson 4 scenario 1
│  │  │  ├─ Lesson42Infographic.png    # Lesson 4 infographic
│  │  │  ├─ Lesson43.png               # Lesson 4 scenario 2
│  │  │  ├─ Lesson43Infographic.png    # Lesson 4 scenario 2 infographic
│  │  │  ├─ Lesson51.png               # Lesson 5 visual aid
│  │  │  ├─ Lesson53.png               # Lesson 5 scenario
│  │  │  ├─ MockPhishingEmail1.png     # Phishing email example
│  │  │  ├─ module1_KnowledgeCheck.pdf # Module 1 knowledge check
│  │  │  ├─ module3scenario2.png       # Module 3 scenario 2
│  │  │  ├─ module3scenario3.png       # Module 3 scenario 3
│  │  │  ├─ Module4Scenario1.png       # Module 4 scenario 1
│  │  │  ├─ Scenario1.png               # General scenario 1
│  │  │  ├─ Secnario3.png              # General scenario 3
│  │  │  ├─ SMSPhishing.png            # SMS phishing example
│  │  │  ├─ social_engineering_in_a_nutshell.png # Overview infographic
│  │  │  └─ Validator_Certification_SocialEngineeringAwareness.pdf # Content validator certification
│  │  └─ Visual_Aid/                   # Visual learning aids and icons
│  │     ├─ Lesson11.png               # Lesson 1 icon
│  │     ├─ Lesson21.png               # Lesson 2 icon
│  │     ├─ Lesson23_ShoulderSurfing.png # Shoulder surfing visual
│  │     ├─ Lesson23_Tailgating.png   # Tailgating visual
│  │     ├─ Lesson31_StrongPassword.png # Strong password visual
│  │     ├─ Lesson32.png               # Lesson 3.2 visual
│  │     ├─ Lesson33.png               # Lesson 3.3 visual
│  │     ├─ Lesson41.png               # Lesson 4.1 visual
│  │     ├─ Lesson42.png               # Lesson 4.2 visual
│  │     ├─ Lesson43.png               # Lesson 4.3 visual
│  │     ├─ Lesson53.png               # Lesson 5.3 visual
│  │     ├─ MockPhishingEmail1.png     # Phishing email visual
│  │     └─ SMSPhishing.png            # SMS phishing visual
│
├─ 🎨 STATIC ASSETS
│  ├─ static/
│  │  ├─ Background.png                # Application background image
│  │  ├─ MMDCLogo.png                  # MMDC institutional logo
│  │  ├─ SEALogo.png                   # Social Engineering Awareness logo
│  │  └─ profile_pictures/             # User profile picture uploads
│     └─ clarkorcullo86_20250807_152047.png # Example profile picture
│
├─ 🔒 SECURITY & DOCUMENTATION
│  ├─ security_middleware.py           # Comprehensive security middleware (CSRF, rate limiting, input validation)
│  ├─ SECURITY_AUDIT_REPORT.md        # Complete security audit documentation
│  ├─ SECURITY_GUIDE.md               # Security implementation guide
│  ├─ env.example                      # Environment variables template
│  ├─ LICENSE                          # MIT License file
│  └─ .gitignore                       # Git ignore patterns
│
├─ 📚 DOCUMENTATION
│  ├─ README.md                        # This comprehensive project documentation
│  ├─ PROJECT_MEMORY.md                # Project development history and decisions
│  ├─ PROJECT_STRUCTURE.md             # Detailed project architecture documentation
│  ├─ APP_STRUCTURE.md                 # Application structure and organization
│  ├─ DEVELOPMENT_GUIDE.md             # Development setup and guidelines
│  ├─ DEPLOYMENT_CHECKLIST.md          # Production deployment checklist
│  ├─ RENDER_DEPLOYMENT.md             # Render.com deployment guide
│  ├─ admin_access_guide.md            # Admin access and management guide
│  └─ VIDEO_FORMAT_STANDARDS.md        # Video content standards and guidelines
│
├─ 📊 LOGS & MONITORING
│  ├─ app.log                          # Application log file (rotates daily)
│  └─ app.log.2025-10-01               # Historical log file (keeps last 3 days)
│
└─ 🐍 PYTHON CACHE
   └─ __pycache__/                     # Python bytecode cache directories
      ├─ app.pyc                       # Compiled app.py
      ├─ config.pyc                    # Compiled config.py
      └─ [other .pyc files]            # Other compiled Python files
```

---

### How content renders (simple flow)

1) You open a module at `/module/<id>`.
2) `app.py` loads your `UserProgress` and latest knowledge‑check score.
3) The page `templates/module.html` renders the module shell and includes a per‑module file from `templates/modules/moduleX.html`.
4) Each `moduleX.html` injects lesson HTML, images, videos, simulations, reflections, and the Knowledge Check button into drawer/accordion items using JavaScript on `DOMContentLoaded`.
5) When you click “Start Knowledge Check”, it goes to `/assessment/<id>`; submitting updates `UserProgress` and marks Completed at ≥80%.
6) Reflections are posted and latest items are shown on the module card and in Admin Dashboard.

---

### Important models (in plain language)

- `UserProgress` (data_models/progress_models.py)
  - Tracks your module status: `not_started`, `in_progress`, `completed`
  - Stores current/highest score and completion timestamp
  - Logic ensures: once you pass (≥80%), status stays Completed
- `AssessmentResult`
  - Stores quiz attempt details (score, total questions, passed)
- `KnowledgeCheckQuestion` and `FinalAssessmentQuestion`
  - Store the multiple‑choice questions for modules and final exam

---

### Admin & analytics
- Admin Dashboard shows: Recent Users (5), Recent Assessments (5), Users Module Reflections (5), and analytics pages.
- Titles stay fixed; lists scroll when there are more items.

---

### Version display
- `/health` returns JSON including `version`.
- Set via the env var `APP_VERSION` (e.g., `1.2.0`). The Admin → System Settings also shows this value.

To change the version
- Locally for testing: set `APP_VERSION` in your environment before running `python app.py`.
- In Render: add/update the Environment Variable `APP_VERSION` in the service settings and redeploy; `/health` and Admin → System Settings will reflect the change.

---

### Policies (recap)
- Knowledge Checks: pass at 80%; unlimited attempts; questions are auto‑seeded for Modules 4 and 5 if needed.
- Final Assessment: exactly 25 questions; pass at 80%.
- Simulations: embedded inside module pages where applicable (no Quick Action buttons for 2–5, per requirements).
- Certificate: must pass Final Assessment AND complete the Satisfaction Survey. Additionally, learners must set a full name in Profile (admins bypass for QA).

---

### Assessment policy (full details)

Knowledge Check (Modules 1–5)
- Purpose: quick check after learning per module
- Question count per attempt: 5
- Question selection:
  - We maintain two question sets per module (Set 1 and Set 2) when available
  - Attempts alternate sets: attempt 1 → Set 1, attempt 2 → Set 2, attempt 3 → Set 1, and so on
  - If a set is missing, all available questions are used and shuffled; we then take the first 5
- Passing score: 80% (4 out of 5)
- Retakes: unlimited
- State after submit:
  - A record is saved in `AssessmentResult` (score, total, correct, passed, answers optional)
  - `UserProgress.update_score(percentage)` is called; if ≥80%, module status becomes Completed
  - Completion is sticky: later attempts below 80% do not downgrade the status
- On module open (`/module/<id>`):
  - We reconcile status. If your latest score was ≥80%, we ensure the badge shows Completed
- Seeding:
  - If a module has no questions, defaults can be seeded; Modules 4 and 5 include auto‑seed helpers

Final Assessment (Cumulative)
- Purpose: capstone evaluation across all modules
- Question count per attempt: 25 (exactly; sampled and shuffled from the pool)
- Passing score: 80%
- Access control:
  - Intended after completing all modules (admins bypass for review)
  - The system checks completed module count before opening the final
- State after submit:
  - A `final_assessment` record is saved with score/answers
  - Passing marks the learner qualified for certification (if enabled)
- Retakes: allowed; previous passes remain recorded

Module completion logic
- A module is Completed when Knowledge Check score ≥80% (some modules may also include simulations in‑page; Quick Action simulation buttons were removed per requirement)
- Completion does not regress on later attempts
- Dashboard computes badges from `UserProgress` and validated completion using `UserService.is_module_fully_completed`

Reflections
- Each module contains a Reflection form
- We display the latest 3 reflections on the module page
- Admin Dashboard shows the latest 5 across all modules in a dedicated box (title fixed; content scrolls)


