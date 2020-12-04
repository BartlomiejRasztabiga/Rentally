#!/usr/bin/env bash

# Exit immediately if pytest exits with a non-zero status.
set -e

# Print commands and their arguments as they are executed.
set -x

pytest --cov=app --cov-report=term-missing app/tests "${@}"
