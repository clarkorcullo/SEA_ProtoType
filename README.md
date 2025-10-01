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

### Configuration
Environment variables (optional):
- `APP_VERSION` — shown in `/health` and Admin → System Settings (e.g., 1.1.0)
- `DATABASE_URL` — use Postgres in production; falls back to SQLite if not set
- `LOG_LEVEL` — default INFO

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

### Credits
Content validated by **Thea Tajonera**, **SANS GIAC GCFA**, from **ANZ**.

Making our digital community safer, one learner at a time.


---

### Project structure (what each folder/file is for)

```text
CapstoneProject_ProtType_Backup/
├─ app.py                      # Main Flask app: routes, seeding, logging, APIs
├─ config.py                   # App configuration (env vars, logging, DB)
├─ requirements.txt            # Python dependencies
├─ runtime.txt                 # Python version for Render
├─ Procfile                    # Render/Gunicorn start command
├─ instance/
│  └─ social_engineering_aw.db # SQLite database (local)
├─ templates/                 # Jinja2 HTML templates (UI)
│  ├─ base.html               # Global layout, header, footer
│  ├─ dashboard.html          # Learner dashboard (cards, progress)
│  ├─ module.html             # Module page (includes per‑module scripts)
│  ├─ assessment/…            # Knowledge check views
│  ├─ admin/…                 # Admin dashboard, users, analytics, settings
│  └─ modules/                # Per‑module runtime content injections
│     ├─ module1.html         # Module 1 content scripts + DOM injection
│     ├─ module2.html         # Module 2 content/scripts (sim, reflection, KC)
│     ├─ module3.html         # Module 3 content/scripts (reference pattern)
│     ├─ module4.html         # Module 4 content/scripts
│     └─ module5.html         # Module 5 content/scripts
├─ data_models/               # Database models (SQLAlchemy)
│  ├─ content_models.py       # Module, KnowledgeCheckQuestion, FinalQuestion
│  ├─ progress_models.py      # UserProgress, AssessmentResult, Reflections
│  └─ user_models.py          # User and auth‑related models
├─ business_services/         # App/business logic by domain
│  ├─ user_service.py         # Completion checks, stats, helpers
│  ├─ module_service.py       # Module utilities
│  ├─ assessment_service.py   # Assessment helpers
│  ├─ analytics_service.py    # Dashboard analytics
│  └─ simulation_service.py   # Simulation payload helpers (placeholders)
├─ helper_utilities/          # Helpers (db persistence, constants, validators)
├─ content_seed/
│  └─ modules.json            # Seed metadata for modules (titles/descriptions)
├─ static/                    # CSS/JS/images served as static assets
├─ learning_modules/          # Learning assets (images, PDFs)
│  ├─ Documents/              # Lesson images, infographics, PDFs
│  └─ Visual_Aid/             # Lesson icons/visual aids
└─ README.md                  # This guide
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

---

### Policies (recap)
- Knowledge Checks: pass at 80%; unlimited attempts; questions are auto‑seeded for Modules 4 and 5 if needed.
- Final Assessment: exactly 25 questions; pass at 80%.
- Simulations: embedded inside module pages where applicable (no Quick Action buttons for 2–5, per requirements).


