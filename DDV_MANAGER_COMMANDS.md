# DDV Manager · Development Commands

Quick reference for running, testing, maintaining, and deploying DDV Manager.

---

# 1. Project

```powershell
cd D:\ddv-manager
```

Project environment:

```text
Python 3.12
.venv
```

Do not use Conda for this project.

---

# 2. First-Time Python Setup

Check installed Python versions:

```powershell
py -0p
```

Create the virtual environment if `.venv` does not exist:

```powershell
py -3.12 -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Check installed packages:

```powershell
pip freeze
```

---

# 3. Backend

Activate the environment:

```powershell
cd D:\ddv-manager
.\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

Stop:

```text
Ctrl + C
```

---

# 4. Frontend

Open a **second PowerShell**.

```powershell
cd D:\ddv-manager\frontend
npm install
npm run dev -- --host 127.0.0.1
```

Frontend:

```text
http://127.0.0.1:5173
```

Stop:

```text
Ctrl + C
```

---

# 5. Daily Startup

### PowerShell 1 · Backend

```powershell
cd D:\ddv-manager
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### PowerShell 2 · Frontend

```powershell
cd D:\ddv-manager\frontend
npm run dev -- --host 127.0.0.1
```

Keep both terminals open while developing.

---

# 6. Production Frontend Build

From the frontend directory:

```powershell
cd D:\ddv-manager\frontend
npm run build
```

Build output:

```text
frontend/dist/
```

Preview the production build:

```powershell
npm run preview
```

---

# 7. SQLite

Open the database:

```powershell
cd D:\ddv-manager
sqlite3 database\ddv_manager.sqlite
```

List tables:

```sql
.tables
```

Inspect common tables:

```sql
SELECT * FROM players;
SELECT * FROM player_characters;
SELECT * FROM characters;
SELECT * FROM roles;
SELECT * FROM player_unlock_sources;
```

Check player character state:

```sql
SELECT
    player_character_id,
    character_id,
    unlocked,
    friendship_level,
    assigned_role,
    role_status
FROM player_characters;
```

Exit:

```sql
.quit
```

---

# 8. Database Migrations

Migration files:

```text
database/migrations/
```

Open SQLite:

```powershell
sqlite3 database\ddv_manager.sqlite
```

Apply a migration:

```sql
.read database/migrations/XXX_migration_name.sql
```

Check the result with SQL.

Exit:

```sql
.quit
```

Do not manually modify the database schema when a migration is required.

---

# 9. API Testing

Start the backend.

Open:

```text
http://127.0.0.1:8000/docs
```

Current important endpoints:

```text
GET  /characters/
GET  /characters/search
GET  /players/
GET  /players/{player_id}/summary
GET  /players/{player_id}/recommendations
PATCH /players/{player_id}/preferences
POST /players/{player_id}/characters
PATCH /players/{player_id}/characters/{character_id}
DELETE /players/{player_id}/characters/{character_id}
GET  /home/
```

Testing workflow:

```text
1. Start backend
2. Open Swagger
3. Run endpoint
4. Check response
5. Fix errors
6. Test again
7. Run frontend
8. Verify UI
```

---

# 10. Python Checks

Check Python:

```powershell
python --version
```

Check which Python is being used:

```powershell
where.exe python
```

Check FastAPI:

```powershell
python -c "import fastapi; print(fastapi.__version__)"
```

Check SQLAlchemy:

```powershell
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

Check Pydantic:

```powershell
python -c "import pydantic; print(pydantic.__version__)"
```

---

# 11. Frontend Checks

From:

```powershell
cd D:\ddv-manager\frontend
```

Install dependencies:

```powershell
npm install
```

Run development server:

```powershell
npm run dev -- --host 127.0.0.1
```

Build:

```powershell
npm run build
```

Preview:

```powershell
npm run preview
```

Check npm version:

```powershell
npm --version
```

Check Node version:

```powershell
node --version
```

---

# 12. Git

From the project root:

```powershell
cd D:\ddv-manager
```

Check status:

```powershell
git status
```

See changes:

```powershell
git diff
```

Stage everything:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Describe the change"
```

Push:

```powershell
git push
```

Recent commits:

```powershell
git log --oneline -10
```

See branches:

```powershell
git branch
```

See remotes:

```powershell
git remote -v
```

---

# 13. Useful Git Recovery Commands

See unstaged changes:

```powershell
git diff
```

See staged changes:

```powershell
git diff --cached
```

Unstage a file:

```powershell
git restore --staged path\to\file
```

Discard changes to a file:

```powershell
git restore path\to\file
```

Check commit history:

```powershell
git log --oneline --decorate --graph -20
```

---

# 14. Troubleshooting

### Frontend says `Failed to fetch`

Check that the backend is running:

```text
http://127.0.0.1:8000/docs
```

Then test the relevant endpoint directly:

```text
http://127.0.0.1:8000/home/
```

If it returns `500 Internal Server Error`, check the Uvicorn terminal for the traceback.

Do not change frontend code until the backend endpoint works directly.

### Backend will not start

Check:

```powershell
cd D:\ddv-manager
.\.venv\Scripts\Activate.ps1
python --version
```

Then:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### PowerShell blocks `.venv` activation

Run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# 15. Deactivate Python

When finished:

```powershell
deactivate
```

---

# 16. Project Rules

- Use the standard `.venv` Python environment.
- Do not use `conda activate .venv`.
- Backend uses FastAPI.
- Database uses SQLite + SQLAlchemy.
- Frontend uses React + TypeScript + Vite.
- Keep game knowledge separate from player state.
- Preserve `Unknown` as a real state.
- Player data is designed to remain local to the player's device/browser.
- Valley Planner is currently **on hold**.
