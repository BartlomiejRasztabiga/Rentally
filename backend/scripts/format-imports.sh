#!/usr/bin/env bash

# Exit immediately if pytest exits with a non-zero status.
set -e

# Print commands and their arguments as they are executed.
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --apply app
sh ./scripts/format.sh
