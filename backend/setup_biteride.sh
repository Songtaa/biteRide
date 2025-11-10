#!/bin/bash
# setup_biteride.sh

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create project structure (if not already created)
mkdir -p app/{core,models,repositories,schemas,services,api/v1/endpoints,dependencies}

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate

# Install core dependencies
uv add "fastapi[standard]" sqlalchemy alembic psycopg2-binary python-jose passlib python-multipart pydantic python-dotenv

# Install dev dependencies
uv add --dev pytest ruff isort flake8

echo "biteRide project setup complete!"
echo "Activate virtual environment: source .venv/bin/activate"
echo "Run application: uv run uvicorn app.main:app --reload"