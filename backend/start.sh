#!/usr/bin/env bash

# Print commands and their arguments as they are executed.
set -x

# Let the DB start
python ./app/pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/seed.py


HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8080}
LOG_LEVEL=${LOG_LEVEL:-info}

# Start Uvicorn without live reload
exec uvicorn --host "$HOST" --port "$PORT" --log-level "$LOG_LEVEL" app.main:app
