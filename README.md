---
title: AI Code Reviewer
emoji: 🔍
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
license: mit
short_description: Reviews AI-generated code for errors, security issues & bugs
---

# AI Code Reviewer

A Streamlit app that reviews AI-generated code (ChatGPT, Claude, Copilot, Gemini…) for:

- 🐛 **Syntax Errors** — code that won't run
- 🧠 **Logic Errors** — flawed algorithms
- 🔒 **Security Vulnerabilities** — injections, hardcoded secrets
- ⚡ **Performance Issues** — O(n²), memory leaks

Results are ranked by severity (Critical → High → Medium → Low → Info) with a 0–100 quality score.

## Setup

Set `ANTHROPIC_API_KEY` in Hugging Face Space secrets.
