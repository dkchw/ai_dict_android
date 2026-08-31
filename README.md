# AI Dict 🤖 📖

Welcome to **AI Dict**, an incredibly smart, highly customizable Android dictionary and linguistics companion powered by advanced Large Language Models (via OpenRouter). 

Designed to go far beyond a simple dictionary, AI Dict acts as a comprehensive language suite that adapts to your needs—whether you're looking up a word, comparing nuances between synonyms, exploring grammar, or rapidly translating concepts into natural, localized expressions.

## ✨ Key Features

* **4 Interactive Modes:**
  * 📚 **Dictionary Mode:** Deep dive into words with pronunciation, synonyms, definitions, and etymology.
  * ⚖️ **Compare Mode:** Compare nuances, register, and collocations between similar words (e.g., *Affect vs. Effect*, *Happy vs. Joyful*).
  * 🗣️ **Translate Mode:** A true "reverse dictionary." Express a concept in your native tongue and let the AI find the exact, natural phrase in your target language.
  * 🧠 **Explain Mode:** Paste entire paragraphs, idioms, or sentences and receive a detailed, sentence-by-sentence linguistic breakdown.
* **Intelligent Swipe Navigation:** Seamlessly swipe left and right between modes using Jetpack Compose's fluid `HorizontalPager`.
* **Isolated Conversations:** Your chat history and ongoing outputs are securely isolated per mode. You can ask a follow-up question in Dict mode, swipe to Translate, and your place is perfectly saved without any data bleed!
* **Auto-Saving Drafts:** Never lose your train of thought. Type a prompt, close the app, and come back—your drafts are instantly restored.
* **Quick External Links:** Instantly bounce from the app to external web dictionaries (like Cambridge or Wikipedia) using a highly customizable URL template setting.
* **Notes & History:** Deeply integrated SQLite (Room) database to save important chats, tag history, and keep persistent Markdown notes of things you've learned. Pull down from anywhere to access your history instantly.
* **Stunning UI & Theming:** Ships with a custom rendering engine that beautifully formats Markdown responses (complete with tables and syntax highlighting) in premium palettes like **Tokyo Night**, Nord, and Dracula.
* **Built-in Auto Updater:** Securely fetches and installs the latest GitHub Releases automatically right from within the app.

## 🚀 Getting Started

### Prerequisites
* Android 8.0 (API level 26) or higher.
* An **OpenRouter API Key** (to power the LLM functionalities).

### Installation
1. Go to the [Releases](https://github.com/dkchw/ai_dict_android/releases) page.
2. Download the latest `ai_dict_vX.X.apk`.
3. Install the APK on your Android device (you may need to allow "Install from Unknown Sources").
4. Open the app, navigate to **Settings** (using the bottom navigation bar), and enter your OpenRouter API Key.

## 🛠️ Configuration & Prompts

AI Dict is a completely customizable platform. From the **Settings** tab, you can override the AI's behavior:
* **Models:** Swap out the engine under the hood. Choose different LLM models for Dictionary, Translate, Compare, and Explain tasks individually!
* **System Prompts:** You aren't locked into the default behavior. Edit the System Prompts directly inside the app to instruct the AI to respond exactly how you want. 
* **Target Languages:** Define custom Target and Source languages natively in the UI.

## 💻 Tech Stack
* **Language:** Kotlin
* **UI Toolkit:** Jetpack Compose & Material Design 3
* **Local Storage:** Room Database (SQLite)
* **Networking:** OkHttp (for HTTP streams and API queries)
* **Architecture:** MVVM (Model-View-ViewModel) with heavily decoupled StateFlows.

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
