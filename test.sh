#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR"

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

pushd "$SCRIPT_DIR" > /dev/null
./.venv/bin/python3 $@
