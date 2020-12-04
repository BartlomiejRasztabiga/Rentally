#!/usr/bin/env bash

# Print commands and their arguments as they are executed.
set -x

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8080}
LOG_LEVEL=${LOG_LEVEL:-info}

# Start Uvicorn with live reload
# shellcheck disable=SC2086
exec uvicorn --reload --host "$HOST" --port "$PORT" --log-level $LOG_LEVEL "$APP_MODULE"
