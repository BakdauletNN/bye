"""Project documentation helper for Smart Dormitory System."""

from textwrap import dedent

PROJECT_NAME = "Smart Dormitory System"
DESCRIPTION = "A Dormitory management system demo for student housing."

API_ENDPOINTS = [
    "/auth/login",
    "/auth/register",
    "/students",
    "/rooms",
    "/applications",
    "/checkins",
    "/analytics/rooms/summary",
]

FRONTEND_OVERVIEW = """
This project contains a minimal frontend under `frontend/` using TypeScript, Vite, HTML, and CSS.
The frontend includes a simple login form and a backend health check for the FastAPI API.
"""

TESTING_NOTE = """
Tests are located in `tests/t.py` and use pytest with httpx to verify the FastAPI app.
Run tests after installing Python dependencies from `requirements.txt`.
"""


def print_docs() -> None:
    print(
        dedent(
            f"""
            {PROJECT_NAME}
            {'=' * len(PROJECT_NAME)}

            {DESCRIPTION}

            API endpoints available:
            {', '.join(API_ENDPOINTS)}

            Frontend:
            {FRONTEND_OVERVIEW.strip()}

            {TESTING_NOTE.strip()}
            """
        )
    )


if __name__ == "__main__":
    print_docs()
