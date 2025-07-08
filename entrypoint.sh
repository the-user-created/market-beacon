#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Default to 'run' if no command is provided
COMMAND=${1:-run}

if [ "$COMMAND" = "run" ]; then
  echo "--> Starting Market Beacon Bot..."
  exec python -m market_beacon "${@:2}"
elif [ "$COMMAND" = "test" ]; then
  echo "--> Running tests inside the container..."
  exec pytest tests/ "${@:2}"
else
  # Allows running arbitrary commands, e.g., 'docker run <image> bash'
  echo "--> Executing command: $*"
  exec "$@"
fi
