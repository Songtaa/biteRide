# biteRide Delivery Backend

## Install uv
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv

## Quick Start
1. cd backend
2. uv venv && source .venv/bin/activate
3. uv add fastapi[standard] sqlalchemy alembic psycopg2-binary
4. python scripts/create_tables.py
5. uvicorn app.main:app --reload
