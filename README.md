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
## Automated Code Review for AI-Generated Code | Claude API + Streamlit

---

## Overview

AI-generated code from tools like ChatGPT, Copilot, Claude, and Gemini is fast but not always correct. This tool reviews AI-generated code automatically — catching syntax errors, logic flaws, security vulnerabilities, and performance issues before they reach production.

Results are ranked by severity with a 0-100 quality score, giving developers an instant assessment of whether AI-generated code is safe to use.

---

## What It Detects

- **Syntax Errors** — code that won't run
- **Logic Errors** — flawed algorithms and incorrect control flow
- **Security Vulnerabilities** — SQL injection, hardcoded secrets, unsafe inputs
- **Performance Issues** — O(n²) complexity, memory leaks, inefficient patterns

---

## Severity Ranking

Every finding is ranked Critical → High → Medium → Low → Info with a 0-100 overall quality score.

---

## How to Run

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Add your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here

python3 -m streamlit run app.py
```

Or deploy directly to Hugging Face Spaces — set `ANTHROPIC_API_KEY` in Space secrets.

---

## Live Demo

Deployed on Hugging Face Spaces. Paste any AI-generated code snippet and get an instant review.

---

*Built by Raja Palagummi | rajapalagummi.com | github.com/rajapalagummi*
