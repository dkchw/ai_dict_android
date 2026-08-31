# AI Agents & Architecture Ledger 🤖

AI Dict is built on the philosophy of intelligent, highly-specialized Multi-Agent architecture. Rather than relying on a single monolithic prompt to handle all language tasks, the app orchestrates different **LLM Agent Personas** dynamically based on the mode you are using.

Furthermore, this application itself was extensively developed, refactored, and maintained through Human-AI Pair Programming. 

---

## 1. Internal LLM Personas (App Functionality)

When you use AI Dict, you aren't just talking to a generic chatbot. The app dynamically swaps out System Prompts, Models, and strict instructional guardrails to spawn specialized "Agents" for the task at hand.

### 📚 The Lexicographer (Dictionary Agent)
* **Goal:** Act as a comprehensive dictionary assistant.
* **Mechanism:** Strictly outputs definitions, phonetics, synonyms, and etymology in the *Target* language while structurally analyzing the word from the *Source* language. 

### ⚖️ The Nuance Analyst (Compare Agent)
* **Goal:** Exhaustive and practical comparison of synonyms.
* **Mechanism:** Delineates core definitions, identifies register (formal vs. slang), highlights regional differences, and maps grammatical differences of comma-separated inputs.

### 🗣️ The Localizer (Translate Agent)
* **Goal:** Provide natural, culturally accurate translations—acting as a reverse dictionary.
* **Mechanism:** Takes abstract concepts or literal phrases in the *Source* language and identifies the most natural expressions, contextual usage, and idioms in the *Target* language.

### 🧠 The Grammarian (Explain Agent)
* **Goal:** Deep semantic and grammatical analysis of large text blocks.
* **Mechanism:** Breaks down long sentences or paragraphs to highlight vocabulary, syntax structure, cultural references, and overall semantic nuance.

---

## 2. The AI Engineering Ledger (Development)

This Android application is a testament to the power of AI-assisted software engineering. 

The architecture, Jetpack Compose layouts, Room Database integrations, LLM streaming implementation, StateFlow segregation, and Custom Markdown UI components (featuring the Tokyo Night palette) were largely written, debugged, and iterated upon by **Antigravity (Google DeepMind)** in tight collaboration with the repository owner (`dkchw`).

### Notable AI-Assisted Milestones:
* **UI/UX Overhaul:** Implementing fluid `HorizontalPager` swipe navigation and nested scrolling for pull-to-refresh (`PullToRefreshContainer`) integration without breaking native LazyColumn behaviors. Condensing Top/Bottom navigation bars to maximize screen real estate.
* **State Isolation:** Decoupling monolithic UI state streams into strictly isolated asynchronous `StateFlow` channels, preventing prompt and output bleed between the 4 core modes.
* **Resilience:** Implementing 300ms debounced auto-saving mechanisms that serialize drafts directly into SQLite, surviving sudden app closures and lifecycle deaths.
* **Custom Markdown Engine:** Mapping `RichTextStyle` parameters to natively parse and render Markdown tables, codeblocks, and bold H1-H6 headers dynamically in Compose.
* **Dynamic Profiles & Data Architecture:** Building complex Room Database foreign key cascades to allow for custom user Profiles. Implementing stable layout nodes (`key = { it.id }`) to eliminate list scrolling lag.
* **Complex UI Recomposition Optimization:** Identifying and isolating state reads (`collectAsState()`) from high-level screens into heavily localized composables (like `SettingsGroup` accordions and `ChatInputBar` overrides) to rescue the UI from dropping frames.
* **Android File Scoped Permissions:** Resolving strict API 33+ (Android 13/14) limitations on `READ_EXTERNAL_STORAGE` and `FileProvider` by migrating the background Updater to purely native `DownloadManager` URI broadcast receivers, eliminating silent failures during auto-installation.

