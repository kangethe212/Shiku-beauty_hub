#!/bin/bash
# Railway migration script - runs migrations automatically
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Migrations and static files ready!"

