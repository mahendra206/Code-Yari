#!/usr/bin/env bash
# Render Build Script for Code Yari Django App
# This script runs during every deployment on Render

set -o errexit  # Exit on error

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running database migrations ==="
python manage.py migrate

echo "=== Build complete! ==="
