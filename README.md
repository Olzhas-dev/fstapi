# Course Catalog API

A standalone FastAPI backend for a small course catalog with filtering, sorting, pagination, and automatic API documentation.

## How to Run

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the development server:

```powershell
fastapi dev main.py
```

Open the API documentation at `http://127.0.0.1:8000/docs`.

## What Was Verified

- `GET /` returns `{"message": "Course Catalog API is running"}`.
- `GET /courses` returns six courses sorted by popularity, with `ai-integration` first and `api-design` last.
- `GET /courses/web-security` returns the Web Security Essentials course.
- `GET /courses/nope` returns a `404` response with `{"detail": "Course not found"}`.
- `GET /courses?is_elective=true` returns two courses: `ai-integration` and `api-design`.
- `GET /courses?is_elective=false` returns four courses: `modern-frontend`, `web-security`, `backend-fastapi`, and `databases-postgresql`.
- `GET /courses?sort=title` returns six courses alphabetically by title: `ai-integration`, `api-design`, `backend-fastapi`, `modern-frontend`, `databases-postgresql`, and `web-security`.
- `GET /courses?page=1&page_size=2` returns `ai-integration` and `modern-frontend`.
- `GET /courses?page=2&page_size=2` returns `web-security` and `backend-fastapi`.
- `GET /courses?page=3&page_size=2` returns `databases-postgresql` and `api-design`.
- `GET /courses?page=4&page_size=2` returns an empty list.
- `/docs` shows exactly three application routes: `GET /`, `GET /courses`, and `GET /courses/{course_id}`.
