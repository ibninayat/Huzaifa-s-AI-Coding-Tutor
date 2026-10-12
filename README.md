# Huzaifa's AI Coding Tutor — AI Coding Tutor

A Streamlit-based AI coding tutor and multi-language online IDE for student learning.

## Features
- Premium dark-themed dashboard and responsive Streamlit layout
- Syntax-highlighted Ace editor with indentation, line numbers, dark theme, and keyboard shortcuts
- Project file explorer: create, switch between, remove, and download files
- Run C, C++, Java, JavaScript, Python, C#, Go, and Rust through Judge0
- Standard input, program output, compile output, stderr, and execution status
- Groq-powered explain, debug, improve, hints, practice generation, and code review
- Local activity history and progress analytics

## Setup (Windows PowerShell)
1. Install Python 3.10+.
2. Open PowerShell in the project folder.
3. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Create your environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
5. Open `.env` in a text editor and add a valid Groq API key to `GROQ_API_KEY`. Never share or upload `.env`.
6. Start the app:
   ```powershell
   python -m streamlit run app.py
   ```

## Environment settings
- `GROQ_API_KEY`: required for AI features
- `GROQ_MODEL`: optional model override
- `JUDGE0_URL`: optional code execution endpoint (defaults to the public Judge0 CE endpoint)
- `JUDGE0_AUTH_TOKEN`: optional token if your Judge0 provider requires one

## Important notes
- Code is sent to the configured Judge0 service for execution. Public service availability, rate limits, privacy terms, and supported language versions may vary.
- This version provides a syntax-highlighted Ace editor embedded in Streamlit. A true VS Code/Monaco experience with multi-file build systems and project-level compilation would require a separate frontend/backend architecture.
- AI-generated code can be wrong. Review and test it before relying on it.
- Never hard-code API keys in source code or commit `.env` to version control.
