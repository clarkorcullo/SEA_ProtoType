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

### Credits
Content validated by **Thea Tajonera**, **SANS GIAC GCFA**, from **ANZ**.

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


