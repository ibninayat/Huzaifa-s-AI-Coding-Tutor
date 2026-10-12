# Huzaifa's AI Coding Tutor — Project Report

## Overview
Huzaifa's AI Coding Tutor is an educational programming workspace built with Python and Streamlit. It combines a multi-language code runner with an AI tutor designed to support beginner and university-level programming students.

## Main Modules
1. **Dashboard** — overview of saved activities, languages used, and recent sessions.
2. **Online IDE** — syntax-highlighted Ace editor, lightweight file explorer, stdin panel, run controls, and output console.
3. **AI Learning Studio** — concept explanations, hints, code explanation, debugging, practice exercises, solution review, and improvement suggestions.
4. **My Progress** — activity history, language statistics, and JSON export.
5. **About** — usage notes, security reminders, and a code self-evaluation checklist.

## Technology Stack
- Python and Streamlit for application logic and UI
- Streamlit Ace for syntax highlighting and editor controls
- Groq API for AI responses
- Judge0 API for sandboxed multi-language code execution
- JSON for local activity history

## Supported Languages
C, C++, Java, JavaScript, Python, C#, Go, and Rust, subject to the configured Judge0 service's available runtimes.

## Limitations
The project file explorer is a lightweight browser-side workspace; it is not a full multi-file compiler or deployment system. Code is sent to the configured Judge0 service. The public execution endpoint may impose limits. A commercial deployment should use managed/self-hosted execution infrastructure, authentication, server-side rate limiting, monitoring, and a separate frontend for a full Monaco editor experience.
