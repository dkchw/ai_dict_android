# AI Agent Guidelines for AI Dict

This document is designed to help autonomous AI agents (like coding assistants) quickly understand the architecture, state management, and critical context of the AI Dict repository when implementing new features or fixing bugs.


## 1. Core Architecture Pattern
*   **FastAPI Backend + React Frontend:** The backend provides REST endpoints and statically serves the Vite-built React frontend.
*   **Build Step Required:** If you modify ANY file in the `frontend/` directory, you MUST run `npm run build` inside the `frontend/` directory. The FastAPI server (`server.py`) serves the compiled assets from `src/ai_dict/static`.
*   **No Hot Reload:** The user generally runs the app via the `ai_dict` command line tool on their host machine, not via `npm run dev`. Therefore, changes to Python files require the user to restart the backend. Changes to frontend files require you to run `npm run build` and then tell the user to refresh their browser.
*   **SPA Routing:** The frontend utilizes `window.history.pushState` for navigation (e.g., `/search`, `/compare`). The backend supports this by utilizing a catch-all route `@app.get("/{full_path:path}")` placed at the ABSOLUTE BOTTOM of `server.py` to return `index.html`. Always ensure new API endpoints are placed ABOVE this catch-all route.


## 2. Database Paradigm
*   **SQLModel / SQLite:** Database interactions are handled via SQLModel.
*   **Location:** The SQLite database is NOT stored in the repository folder. It is stored in the user's local data directory (e.g., `~/.local/share/ai_dict/ai_dict.db`).
*   **Schema Migrations:** There is no Alembic setup. If you add a column to a table in `db.py`, you must write a script to execute the raw `ALTER TABLE` SQL command to update the live user database, otherwise the backend will crash on the next query.
*   **Object Staleness:** Beware of `session.commit()` expiring objects. If you need to return a dictionary of an object via `.model_dump()` after a commit, ensure you call `session.refresh(object)` first.
*   **Profiles:** All major data tables (`Word`, `Comparison`, `Explain`, `Translation`) include a `profile_id` foreign key. The active profile restricts what history is visible.

## 3. Frontend State Management
*   **Global State (`App.jsx`):** Tab management (`searchTabs`, `compareTabs`, `explainTabs`, `translationTabs`) and global history arrays (`words`, `comparisons`, `explains`, `translations`) are managed in `App.jsx`.
*   **Local State:** Individual tab contents and interactions are managed inside `SearchTab.jsx`, `CompareTab.jsx`, `ExplainTab.jsx`, and `TranslationTab.jsx`.
*   **Tab Synchronization:** `SearchTab` communicates its title and loading state back to `App.jsx` via the `onUpdateTab` callback prop.

## 4. UI/UX Rules
*   **TailwindCSS:** Use standard Tailwind utility classes for styling. Follow the existing Dark Mode (`dark:`) patterns.
*   **Responsive Design:** Ensure panels and popups work on narrow screens. Avoid relying on hardcoded viewport limits for layout. Use CSS `flex`, `truncate`, and responsive positioning.
*   **Hover Components:** The `HoverReviewPopup` uses `fixed` positioning and calculates its coordinates against the viewport bounds (`window.innerWidth`, `window.innerHeight`) to prevent clipping by overflow containers. Keep this paradigm intact if modifying popups.

## 5. Working with the LLM Integration (`ai.py`)
*   **OpenRouter:** The backend interacts asynchronously with the OpenRouter API.
*   **Regex Extractors:** We rely on specific markdown patterns to extract `Language` and `Base form (lemma)` from the AI response. If you change the system prompt in `ai.py` or `config.py`, ensure the regex patterns in `extract_language_and_lemma()` continue to match correctly, or update them.

## Example Workflow for an Agent
1. User requests a feature.
2. Edit Python backend `server.py` or `db.py`. (If `db.py` changed, run an `ALTER TABLE` via python script against the live DB).
3. Edit React components in `frontend/src/`.
4. Run `cd frontend && npm run build`.
5. Instruct user to restart the backend (if Python changed) and refresh the browser.
