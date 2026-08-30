import re

with open("README.md", "r") as f:
    content = f.read()

features_addition = """## Features

*   **Intelligent Word Search:** Get comprehensive explanations for any word in any language. Explicitly configure your target and source languages if desired.
*   **Word Comparison:** Compare two or more words to understand their subtle differences in meaning, register, and usage contexts.
*   **Text Explanation:** Paste a sentence or paragraph to get a breakdown of grammar, vocabulary, and meaning.
*   **Deep Translation:** Translates texts with high nuance and precision between any languages.
*   **Follow-up Chat:** Chat with the AI directly within a search result to ask follow-up questions or clarify doubts.
*   **Profiles & History:** Organize your learning via Profiles (e.g., "Spanish Learning", "Work"). Automatically groups your searches by day or by active "Study Session", allowing you to track and manage what you learn.
*   **Seamless Backups (ZIP):** Export and import your entire database (including settings, profiles, and history) via a single click in the Settings tab.
*   **Interactive UI:** Modern React frontend with dark mode support, horizontal tab scrolling, and a seamless "Hover Review" system that lets you peek at past searches instantly.
*   **External Integrations:** Configure dynamic links to external dictionaries (like Wiktionary or Cambridge) based on the detected language.
*   **Local Data Privacy:** All history and chat data is stored locally in an SQLite database on your machine.
*   **Customizable AI:** Configure the system prompt, main LLM, and fallback LLMs via the Settings panel."""

content = re.sub(r'## Features\n.*?## Architecture', features_addition + '\n\n## Architecture', content, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(content)
