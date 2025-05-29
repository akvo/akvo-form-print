#!/bin/bash
set -e

echo "Running tests..."
pytest --cov=AkvoFormPrint --cov-report=term-missing
