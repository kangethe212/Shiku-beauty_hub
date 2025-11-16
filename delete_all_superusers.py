#!/usr/bin/env python
"""
Delete all superusers from both local SQLite and Railway PostgreSQL databases
"""
import os
import sys

# Set Railway database URL BEFORE Django loads
RAILWAY_PUBLIC_DB = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.db import connections
from django.conf import settings
import dj_database_url

print("=" * 70)
print("  DELETING ALL SUPERUSERS FROM ALL DATABASES")
print("=" * 70)

# Step 1: Delete from local SQLite
print("\n[1/2] Deleting superusers from local SQLite database...")
local_superusers = User.objects.filter(is_superuser=True)
local_count = local_superusers.count()
print(f"  ✓ Found {local_count} superusers in local database")

if local_count > 0:
    print("\n  Local Superusers to be deleted:")
    for user in local_superusers:
        print(f"    - {user.username} ({user.email or 'No email'})")
    
    # Delete them
    deleted_count = local_superusers.delete()[0]
    print(f"\n  ✓ Deleted {deleted_count} superuser(s) from local database")
else:
    print("  ✓ No superusers found in local database")

# Step 2: Delete from Railway PostgreSQL
print(f"\n[2/2] Deleting superusers from Railway PostgreSQL...")
railway_db = dj_database_url.config(default=RAILWAY_PUBLIC_DB)

# Verify it's PostgreSQL
engine = railway_db.get('ENGINE', '')
if 'postgres' not in engine.lower():
    print(f"❌ Error: Not a PostgreSQL database! Got: {engine}")
    sys.exit(1)

print(f"  ✓ Database engine: {engine}")
print(f"  ✓ Host: {railway_db.get('HOST', 'Unknown')}")
print(f"  ✓ Database: {railway_db.get('NAME', 'Unknown')}")

# Connect to Railway
original_db = settings.DATABASES['default']
settings.DATABASES['railway'] = railway_db
settings.DATABASES['default'] = railway_db

# Close existing connections
connections.close_all()

try:
    conn = connections['default']
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        print("  ✓ Connected to Railway PostgreSQL")
    
    # Get Railway superusers
    railway_superusers = User.objects.using('default').filter(is_superuser=True)
    railway_count = railway_superusers.count()
    print(f"  ✓ Found {railway_count} superuser(s) in Railway database")
    
    if railway_count > 0:
        print("\n  Railway Superusers to be deleted:")
        for user in railway_superusers:
            print(f"    - {user.username} ({user.email or 'No email'})")
        
        # Delete them
        deleted_count = railway_superusers.delete()[0]
        print(f"\n  ✓ Deleted {deleted_count} superuser(s) from Railway database")
    else:
        print("  ✓ No superusers found in Railway database")
    
    # Final verification
    remaining_superusers = User.objects.using('default').filter(is_superuser=True).count()
    print(f"\n  ✓ Remaining superusers in Railway: {remaining_superusers}")
    
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)
finally:
    # Restore original database
    settings.DATABASES['default'] = original_db

# Final summary
print("\n" + "=" * 70)
print("  ✅ SUPERUSER DELETION COMPLETE!")
print("=" * 70)

# Verify local database
local_remaining = User.objects.filter(is_superuser=True).count()
print(f"\nSummary:")
print(f"  - Remaining superusers in local database: {local_remaining}")
print(f"  - Remaining superusers in Railway database: {remaining_superusers}")

if local_remaining == 0 and remaining_superusers == 0:
    print("\n✓ All superusers have been deleted from both databases.")
    print("  You can now create a new superuser using:")
    print("    python manage.py createsuperuser")
else:
    print("\n⚠️  Warning: Some superusers may still exist. Please verify manually.")

print("\n" + "=" * 70)

