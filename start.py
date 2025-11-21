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

# Setup Maina as superadmin
print("=" * 50)
print("Setting up Maina superadmin...")
print("=" * 50)
try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
    django.setup()
    from django.contrib.auth.models import User
    
    maina, created = User.objects.get_or_create(
        username='Maina',
        defaults={
            'email': 'bennymaish01@gmail.com',
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
        }
    )
    maina.email = 'bennymaish01@gmail.com'
    maina.is_superuser = True
    maina.is_staff = True
    maina.is_active = True
    maina.set_password('Benny@123')
    maina.save()
    
    if created:
        print("✓ Created Maina superadmin")
    else:
        print("✓ Updated Maina superadmin")
    print("  Username: Maina")
    print("  Password: Benny@123")
except Exception as e:
    print(f"⚠ Warning: Could not setup Maina admin: {e}")

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

