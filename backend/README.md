# biteRide Delivery Backend

## Quick Start
1. cd backend
2. uv venv && source .venv/bin/activate
3. uv add fastapi[standard] sqlalchemy alembic psycopg2-binary
4. python scripts/create_tables.py
5. uvicorn app.main:app --reload
