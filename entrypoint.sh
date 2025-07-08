#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Default to 'run' if no command is provided
COMMAND=${1:-run}

if [ "$COMMAND" = "run" ]; then
  echo "--> Starting Market Beacon Bot..."
  # This assumes your main application logic is in src/main.py
  # The 'exec' command replaces the shell process with the Python process,
  # which is better for signal handling (e.g., Ctrl+C).
  exec python -m market_beacon.main "${@:2}"
elif [ "$COMMAND" = "test" ]; then
  echo "--> Running tests inside the container..."
  exec pytest tests/ "${@:2}"
else
  # Allows running arbitrary commands, e.g., 'docker run <image> bash'
  echo "--> Executing command: $*"
  exec "$@"
fi
