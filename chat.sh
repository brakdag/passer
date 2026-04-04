#!/bin/bash
# Define absolute path to project root
PROJECT_ROOT="/mnt/DataSD/sandbox/charla"
export PYTHONPATH="$PROJECT_ROOT"
"$PROJECT_ROOT/venv/bin/python" -m passer.main
