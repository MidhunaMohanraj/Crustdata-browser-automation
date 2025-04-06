# Crustdata Build Challenge - Level 1

This project implements an `/interact` API using FastAPI and Playwright to control browser actions via natural language commands.

## ✅ Features

- Open websites
- Search queries on any site (Google, Bing, Amazon, YouTube, etc.)
- Simulate Gmail login
- Click on specific search results
- Custom error handling

## 🚀 Run Locally

```bash
pip install -r requirements.txt
playwright install
uvicorn main:app --reload
