import re

with open("AGENTS.md", "r") as f:
    content = f.read()

# Add information about Profiles and Routing
architecture_addition = """
## 1. Core Architecture Pattern
*   **FastAPI Backend + React Frontend:** The backend provides REST endpoints and statically serves the Vite-built React frontend.
*   **Build Step Required:** If you modify ANY file in the `frontend/` directory, you MUST run `npm run build` inside the `frontend/` directory. The FastAPI server (`server.py`) serves the compiled assets from `src/ai_dict/static`.
*   **No Hot Reload:** The user generally runs the app via the `ai_dict` command line tool on their host machine, not via `npm run dev`. Therefore, changes to Python files require the user to restart the backend. Changes to frontend files require you to run `npm run build` and then tell the user to refresh their browser.
*   **SPA Routing:** The frontend utilizes `window.history.pushState` for navigation (e.g., `/search`, `/compare`). The backend supports this by utilizing a catch-all route `@app.get("/{full_path:path}")` placed at the ABSOLUTE BOTTOM of `server.py` to return `index.html`. Always ensure new API endpoints are placed ABOVE this catch-all route.
"""

content = re.sub(r'## 1\. Core Architecture Pattern\n.*?## 2', architecture_addition + '\n## 2', content, flags=re.DOTALL)

db_addition = """
## 2. Database Paradigm
*   **SQLModel / SQLite:** Database interactions are handled via SQLModel.
*   **Location:** The SQLite database is NOT stored in the repository folder. It is stored in the user's local data directory (e.g., `~/.local/share/ai_dict/ai_dict.db`).
*   **Schema Migrations:** There is no Alembic setup. If you add a column to a table in `db.py`, you must write a script to execute the raw `ALTER TABLE` SQL command to update the live user database, otherwise the backend will crash on the next query.
*   **Object Staleness:** Beware of `session.commit()` expiring objects. If you need to return a dictionary of an object via `.model_dump()` after a commit, ensure you call `session.refresh(object)` first.
*   **Profiles:** All major data tables (`Word`, `Comparison`, `Explain`, `Translation`) include a `profile_id` foreign key. The active profile restricts what history is visible.
"""

content = re.sub(r'## 2\. Database Paradigm\n.*?## 3', db_addition + '\n## 3', content, flags=re.DOTALL)

with open("AGENTS.md", "w") as f:
    f.write(content)
