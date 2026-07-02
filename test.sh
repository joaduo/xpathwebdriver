#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR"

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

PYTHON=".venv/bin/python3"

if [ ! -f "$PYTHON" ]; then
    echo "Virtual environment not found, using system python"
    PYTHON="python3"
fi

pushd "$SCRIPT_DIR" > /dev/null
    $PYTHON "$@"
popd > /dev/null
