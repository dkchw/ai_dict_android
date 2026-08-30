import re

with open("TECHNICAL_SPECS.md", "r") as f:
    content = f.read()

# Add translation schemas and profile
schema_addition = """### Core Models
- `Profile`: User profiles. Fields: `id`, `name`, `rank`, `is_default`, `created_at`.
- `Word`: Dictionary lookup. Fields: `id`, `term`, `language`, `lemma`, `search_count`, `color`, `session_id`, `profile_id`, `created_at`, `updated_at`.
- `ChatMessage`: Follow-up messages. Fields: `id`, `word_id`, `role`, `content`, `session_id`, `created_at`.
- `Comparison`: Word comparison. Fields: `id`, `words`, `explanation`, `session_id`, `profile_id`, `created_at`.
- `ComparisonChat`: Comparison follow-up messages.
- `Explain`: Text explanation. Fields: `id`, `text`, `explanation`, `session_id`, `profile_id`, `created_at`.
- `ExplainChat`: Text explanation follow-ups.
- `Translation`: Text translations. Fields: `id`, `source_text`, `source_lang`, `target_lang`, `translation`, `session_id`, `profile_id`, `created_at`.
- `TranslationChat`: Translation follow-ups.
- `AppSetting`: Key-value store for app configuration (API keys, default languages).
- `ExternalLinkTemplate`: User-defined templates for external dictionary links."""

content = re.sub(r'### Core Models\n.*?\n## 4', schema_addition + '\n\n## 4', content, flags=re.DOTALL)

# Add Profile Endpoints and Zip Export
api_addition = """### Sessions & Profiles
- `GET /api/profiles`: Get all user profiles ordered by rank.
- `POST /api/profiles`: Create a new profile.
- `PATCH /api/profiles/{id}/rename`: Rename a profile.
- `PATCH /api/profiles/{id}/set_default`: Set a profile as the undeletable default.
- `POST /api/profiles/reorder`: Reorder profiles by rank.
- `DELETE /api/profiles/{id}`: Delete a profile and all its associated history.
- `DELETE /api/sessions/{session_id}`: Deletes all items belonging to a specific session.

### Data Management & Settings
- `GET /api/data/export_zip`: Generates a timestamped `.zip` containing the SQLite database.
- `POST /api/data/import_zip`: Uploads a `.zip` file, extracting and replacing the live `ai_dict.db`.
- `POST /api/settings`: Update a specific app setting."""

content = re.sub(r'### Sessions & Data Management\n.*?\n## 5', api_addition + '\n\n## 5', content, flags=re.DOTALL)

with open("TECHNICAL_SPECS.md", "w") as f:
    f.write(content)
