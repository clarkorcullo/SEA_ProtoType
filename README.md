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


