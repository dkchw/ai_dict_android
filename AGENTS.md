# AI Agents & Architecture Ledger 🤖

AI Dict is built on the philosophy of intelligent, highly-specialized Multi-Agent architecture. Rather than relying on a single monolithic prompt to handle all language tasks, the app orchestrates different **LLM Agent Personas** dynamically based on the mode you are using.

Furthermore, this application itself was extensively developed, refactored, and maintained through Human-AI Pair Programming. 

---

## 1. Internal LLM Personas (App Functionality)

When you use AI Dict, you aren't just talking to a generic chatbot. The app dynamically swaps out System Prompts, Models, and strict instructional guardrails to spawn specialized "Agents" for the task at hand.

### 📚 The Lexicographer (Dictionary Agent)
* **Goal:** Comprehensive dictionary and active language production assistant.
* **Mechanism:** Anchored on the principle of *Production Over Recognition*, it structurally analyzes source inputs (words, phrases, collocations) while strictly delivering explanations, definitions, etymology, chunks/collocations, verb patterns/prepositions, phrasal verbs, circumlocutions/paraphrases, and active retrieval production drills in the *Target* language. 

### ⚖️ The Nuance Analyst (Compare Agent)
* **Goal:** Exhaustive and practical comparison of synonyms.
* **Mechanism:** Delineates core definitions, identifies register (formal vs. slang), highlights regional differences, and maps grammatical differences of comma-separated inputs.

### 🗣️ The Localizer (Translate Agent)
* **Goal:** Provide natural, culturally accurate translations—acting as a reverse dictionary.
* **Mechanism:** Takes abstract concepts or literal phrases in the *Source* language and identifies the most natural expressions, contextual usage, and idioms in the *Target* language.

### 🧠 The Grammarian (Explain Agent)
* **Goal:** Deep semantic and grammatical analysis of large text blocks.
* **Mechanism:** Breaks down long sentences or paragraphs to highlight vocabulary, syntax structure, cultural references, and overall semantic nuance.

### ✍️ The Stylist & Interpreter (Correct Agent)
* **Goal:** Dual-phase grammar refinement and contextual interpretation.
* **Mechanism:** Orchestrates a strict pipeline consisting of a **Corrector Phase** (detects errors, crafts an Improved Natural Edition in the source language, and explains linguistic choices) followed optionally by a **Translator Phase** (generates the Best Translation with vocabulary and sentence structure analysis). Supports user-toggled "Correction and Translation" vs "Correction-Only" modes, persistent language preferences per profile, and language-code marker heuristics (e.g. `de-`, `-deu`).

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
* **Granular Reasoning Engine Control:** Implemented independent reasoning effort controls (`default`, `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`) per model and profile scope, seamlessly interfacing with OpenRouter's Reasoning API while preserving fallback safety and custom inheritance.
* **Resilient 24/7 Background Service & Two-Way State Sync:** Engineered a foreground service with watchdog self-healing and bidirectional state synchronization. Notification action callbacks ("Stop 24/7 Mode") write directly to Room SQLite and trigger reactive Compose `LaunchedEffect` updates to guarantee UI switches never desynchronize from the actual service lifecycle.
* **Smart Mode Routing & Cross-Mode Regeneration Engine:** Integrated dynamic sentence-length heuristic routing for text-selection popups (queries > 3 words automatically target `explain` mode with instant streaming). Implemented universal cross-mode migration across Dictionary, Compare, Translate, and Explain with automatic prompt adaptation and live stream regeneration directly accessible from action bars and history cards.
* **Resilient Reactive History & Live Streaming Dashboard:** Completely redesigned History architecture by decoupling mode queries from Pager indices, preventing history zeroing/disappearance during background generation. Engineered a reactive Mode Filter Bar (`Dict`, `Compare`, `Translate`, `Explain`), live "Generating..." card indicators, and in-place real-time Markdown streaming within the History inspection panel.
* **Instant Intent Search & Strict Mode-Independent History Segregation:** Eliminated text selection popup stale input locks by enforcing fresh intent overrides and multi-intent triggers across `onCreate` and `onNewIntent`. Re-engineered the History architecture into strictly isolated, independent streams per mode (`Dict`, `Compare`, `Translate`, `Explain`), eliminating mode mixing while synchronizing active mode context directly from navigation entry points.
* **Resilient 24/7 Background Engine & Robust WakeLock Architecture:** Re-architected the 24/7 background foreground service with non-leaking, synchronized `PARTIAL_WAKE_LOCK` management for uninterrupted LLM network streaming during sleep. Restored notification dismissal resurrection (`ACTION_NOTIFICATION_DISMISSED`) and a lightweight 15-second watchdog to keep the 24/7 foreground service alive across aggressive OEM task killers, while fully aligning `FOREGROUND_SERVICE_SPECIAL_USE`, `WAKE_LOCK`, and `REQUEST_INSTALL_PACKAGES` permissions.
* **The Fifth Agent ("Correct" Mode) & Persistent Multi-Mode Engine:** Architected and integrated the fifth specialized agent ("Correct") combining dual-phase grammar correction and contextual translation according to `Fifth_Mode.md`. Implemented seamless in-place switching between "Correction and Translation" and "Correction-Only" modes with remembered profile preferences, 300ms debounced draft persistence (`CORRECT_DRAFT`), isolated `SearchState` streams, independent history counters and filters, custom profile AI model/reasoning/prompt configurations, and universal cross-mode regeneration.
* **Chat Header Ellipsis, Full-Text Inspector & In-Place Rename Engine:** Resolved chat header UI bleeding and layout truncation caused by multi-line paragraph queries. Implemented single-line ellipsis (`maxLines = 1, overflow = TextOverflow.Ellipsis`) headers with visual edit pencil indicators (`ChatHeaderTitle`) across Dictionary, Compare, Translate, Explain, and Correct modes, as well as the History inspection pane. Integrated a comprehensive dialog (`RenameWordDialog`) enabling users to inspect the complete, untruncated original query in a scrollable container and immediately rename chats in-place with real-time SQLite and reactive StateFlow synchronization, bypassing the need to navigate to History.
* **Production-Centric Dictionary Engine & Global Prompt Overhaul:** Upgraded the default global Lexicographer prompt according to `Update_Dict_Prompt.md`. Enforces mandatory target explanation language compliance without English fallbacks when non-English target languages are selected, embeds natural multi-word chunks and collocations, verb-preposition patterns, common phrasal verbs, circumlocution/paraphrase fallbacks, and active retrieval production drills (idea → source language) to foster active spoken and written language production over passive recognition.
* **Default Model Modernization (`deepseek/deepseek-v4-flash-0731`):** Migrated the global and profile default models across all agents (Dictionary, Compare, Translate, Explain, Correct, Chat) to `deepseek/deepseek-v4-flash-0731`. Added seamless automatic database migration on startup to transition existing saved SQLite configurations to the new snapshot while preserving fallback redundancy with `google/gemini-3.8-flash`.
* **On-Device Local Machine Translation & Android System Translator Provider:** Engineered an independent offline Machine Translation (MT) engine powered by Google ML Kit and offline Opus-MT with dual tier selection: Normal (Instant, offline) vs Strong (NLLB-200). Integrated seamless local translation directly inside Correct mode (`correctType = "machine_translate"`) with remembered profile preferences and one-click "Deepen with AI LLM" transition. Registered AI Dict as an official Android system translation provider (`android.intent.action.TRANSLATE` and `PROCESS_TEXT`) featuring a standalone, floating Google-Translate style overlay dialog (`TranslateActivity`) with real-time translation, language swap, TTS pronunciation, copy tools, and instant deep-dive routing into AI Dict's LLM personas.
* **Dedicated Translator UI, Offline Model Manager & History MT Isolation:** Overhauled the on-device Local MT interface inside Correct mode into a dedicated translator layout featuring interactive Source and Target cards, language swap, TTS pronunciation audio, and instant clipboard tools. Added comprehensive on-device offline model management (`ManageOfflineModelsDialog`) with download/deletion of ~30MB language packs, storage tracking, and Wi-Fi preferences accessible from both the app and system translate overlay. Enforced transient memory by default so offline machine translations are not saved to SQLite automatically, while offering explicit one-tap bookmarking and "✨ Deepen with AI LLM" handoffs. Styled saved MT history cards with distinct cyan accents (`#06B6D4`), `LOCAL MT` badges, and dedicated `🌐 MT Only` filtering.



