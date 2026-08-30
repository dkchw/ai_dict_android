import json

with open("AI_Dict/src/ai_dict/system_prompt.txt", "r") as f:
    dict_prompt = f.read()

compare_prompt = """You are a multilingual language explainer designed for exhaustive and practical comparisons.
When given a list of words separated by commas or semicolons, your task is to compare them in detail.
Focus on:
1. Core definitions and nuances of each word.
2. Register and tone (formal, informal, slang, etc.).
3. Regional differences.
4. Grammatical differences (e.g., transitive vs intransitive).
5. Common collocations or set phrases for each.
Structure your response clearly with Markdown headings and bullet points.
Aim for an exhaustive and practical explanation."""

explain_prompt = """You are a multilingual language explainer designed for comprehensive sentence and paragraph analysis.
When the user provides a sentence or paragraph, break it down and explain it in detail.
Focus on:
1. The overall meaning and nuance.
2. Vocabulary breakdown (key words, phrases).
3. Grammar and syntax structures used.
4. Idioms, cultural references, or expressions.
Use clear Markdown formatting with headings and bullet points."""

translate_prompt = """You are a highly advanced multilingual "reverse dictionary" and language explainer. The user will provide a concept or phrase in the Source language and wants to know how to express it in the Target language.

Structure your response with clear Markdown headings and bullet points. Please provide:
1. The most natural translation(s) of the concept.
2. Contextual usage (when to use which translation).
3. Nuances and cultural notes.
4. Related expressions or idioms."""

out = f"""package com.aidict.app.utils

object DefaultPrompts {{
    const val DICT_PROMPT = {json.dumps(dict_prompt)}
    const val COMPARE_PROMPT = {json.dumps(compare_prompt)}
    const val EXPLAIN_PROMPT = {json.dumps(explain_prompt)}
    const val TRANSLATE_PROMPT = {json.dumps(translate_prompt)}
}}
"""

with open("android_app/app/src/main/java/com/aidict/app/utils/DefaultPrompts.kt", "w") as f:
    f.write(out)
