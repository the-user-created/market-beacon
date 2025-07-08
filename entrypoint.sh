#!/bin/bash

MAKE=null
COMMAND_ARGS=""

terminate() {
    echo "Received termination signal. Forwarding to child processes..."
    pkill -TERM -P $$
    wait
}

trap terminate SIGTERM SIGINT

while test $# -gt 0; do
  case "$1" in
    -mk=*|--make=*)
      set_argument="$1"
      MAKE="${set_argument//*=/}"
      shift
      ;;
    *)
      echo "Error: Unexpected Argument: $1"
      exit 1
      ;;
  esac
done

echo "Running make command with arguments:"
echo "MAKE                    =    ${MAKE}"
echo "COMMAND_ARGUMENTS       =    ${COMMAND_ARGS}"

if [ "$MAKE" = "execute-tests" ]; then
  make "$MAKE"
elif [ "$MAKE" = "run" ]; then
  make "$MAKE" args="$COMMAND_ARGS"
else
  echo "Error: Invalid make command"
  exit 1
fi

wait
