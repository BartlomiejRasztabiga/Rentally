#! /usr/bin/env bash
set -e

python3 /app/app/tests_pre_start.py

bash ./scripts/test.sh "$@"
