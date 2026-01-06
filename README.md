Arkan Backend (FastAPI) Scaffold

Overview
- FastAPI backend scaffold prepared to migrate Arkan Next.js API routes.
- Includes JWT auth (custom), WebSocket/SSE samples, and modular routers.
- Intentionally light DB layer until we confirm your database. Hooks are ready for SQLAlchemy/SQLModel.

Quick start
1) Python env
   - Python 3.11+
   - pip install -r requirements.txt
2) Run
   - cp .env.example .env  # adjust values
   - uvicorn app.main:app --reload
3) Open http://localhost:8000/docs

Project layout
- app/
  - main.py                # App factory, middlewares, router include
  - api/v1/                # Versioned API modules
    - __init__.py
    - router.py            # Root v1 router
    - health.py            # Health checks
    - auth.py              # Login/refresh/logout using custom JWT
    - users.py             # Example CRUD and patterns
    - realtime.py          # WebSocket and SSE endpoints
  - core/
    - config.py            # Env settings via pydantic
    - security.py          # JWT utils (encode/decode), password hashing
    - logging.py           # Structured logging setup
  - db/
    - session.py           # DB session factory (placeholder)
    - models.py            # SQLAlchemy models (placeholder)
    - repository.py        # Example repository base
  - schemas/
    - auth.py              # Pydantic models for auth
    - users.py             # Pydantic models for users
    - common.py
  - services/
    - users.py             # Business logic example
  - dependencies.py        # DI helpers
- tests/                   # Pytest tests (basic)
- requirements.txt         # Dependencies
- .env.example             # Environment configuration
- Dockerfile               # Container build
- docker-compose.yml       # Optional: app + db + redis (commented DB until chosen)

How to mirror Next.js APIs
1) Inventory your routes
   - App router: src/app/api/**/route.ts exports GET/POST/PUT/PATCH/DELETE
   - Pages router: src/pages/api/**/* exports default handler
2) For each endpoint, add a FastAPI route in app/api/v1/*.py with identical:
   - path, method(s), query/body/headers
   - status codes and JSON shape
   - auth guards (JWT) if required
3) Place shared logic in services/ and repositories/.

Database
- session.py is ready to accept SQLAlchemy engine once DB decided.
- Add your models to db/models.py and run Alembic (to be added after DB selection).

Realtime
- app/api/v1/realtime.py exposes WebSocket and SSE examples.
- Adjust channel names and auth checks to match the current app.

Next steps once we confirm DB
- Add SQLAlchemy + Alembic and wire repositories.
- Replace in-memory stores in users service with DB.

Contributing
- lint: ruff .
- test: pytest -q

