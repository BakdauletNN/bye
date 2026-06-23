# Smart Dormitory System

A demo student dormitory management system with a FastAPI backend and a minimal TypeScript frontend.

## Project Layout

- `src/` — FastAPI backend application and database models.
- `frontend/` — Static frontend built with Vite, TypeScript, HTML, and CSS.
- `tests/` — Basic pytest test suite for FastAPI endpoints.
- `docs/hi.py` — Documentation helper script describing the project.

## Backend

Install Python dependencies and run the API server:

```bash
python -m pip install -r requirements.txt
uvicorn src.main:app --reload
```

The backend exposes routes like:

- `POST /auth/login`
- `POST /auth/register`
- `GET /students`
- `GET /rooms`
- `POST /applications`
- `POST /checkins`
- `GET /analytics/rooms/summary`

## Frontend

Install the frontend dependencies and start the development server:

```bash
cd frontend
npm install
npm run dev
```

Open the browser at the URL shown by Vite. The frontend includes a login form and a backend health check.

## Tests

Install test dependencies and run pytest:

```bash
python -m pip install -r requirements.txt
pytest tests/t.py
```

## Documentation

Run `python docs/hi.py` to print a short project overview.
