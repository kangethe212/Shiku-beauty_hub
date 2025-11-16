#!/usr/bin/env python
"""
Railway startup script - runs migrations and starts Gunicorn
"""
import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Warning: {description} failed with code {result.returncode}")
        # Don't exit - continue anyway
    return result.returncode

# Run migrations before starting server
print("=" * 50)
print("Railway Startup - Running Pre-flight Checks")
print("=" * 50)

# Check if DATABASE_URL is set
database_url = os.environ.get('DATABASE_URL')
if database_url:
    print(f"✓ DATABASE_URL detected: {database_url[:20]}...")
    # Run migrations
    run_command("python manage.py migrate --noinput", "Database migrations")
else:
    print("⚠ WARNING: DATABASE_URL not set - using SQLite fallback")
    print("  Make sure PostgreSQL is added in Railway dashboard")
    # Still try to run migrations (for SQLite)
    run_command("python manage.py migrate --noinput", "Database migrations")

# Collect static files
run_command("python manage.py collectstatic --noinput", "Collecting static files")

print("=" * 50)
print("Starting Gunicorn server...")
print("=" * 50)

# Start Gunicorn
port = os.environ.get('PORT', '8000')
cmd = [
    'gunicorn',
    'her_beauty_hub.wsgi:application',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '2',
    '--threads', '2',
    '--timeout', '60'
]

sys.exit(subprocess.call(cmd))

