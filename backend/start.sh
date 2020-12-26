#!/usr/bin/env bash

# Print commands and their arguments as they are executed.
set -x

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8080}
LOG_LEVEL=${LOG_LEVEL:-info}

# Start Uvicorn without live reload
exec uvicorn --host "$HOST" --port "$PORT" --log-level "$LOG_LEVEL" app.main:app
