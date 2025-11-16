#!/usr/bin/env python
"""
Sync all users from local SQLite database to Railway PostgreSQL
Ensures all users (including superusers) are transferred
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
print("  SYNCING USERS TO RAILWAY POSTGRESQL")
print("=" * 70)

# Step 1: Get users from local SQLite
print("\n[1/4] Reading users from local SQLite database...")
local_users = User.objects.all()
local_count = local_users.count()
print(f"  ✓ Found {local_count} users in local database")

if local_count == 0:
    print("\n⚠️  No users found in local database!")
    sys.exit(0)

# Display local users
print("\n  Local Users:")
for user in local_users:
    print(f"    - {user.username} ({user.email or 'No email'}) - Superuser: {user.is_superuser}")

# Step 2: Configure Railway PostgreSQL
print(f"\n[2/4] Configuring Railway PostgreSQL connection...")
railway_db = dj_database_url.config(default=RAILWAY_PUBLIC_DB)

# Verify it's PostgreSQL
engine = railway_db.get('ENGINE', '')
if 'postgres' not in engine.lower():
    print(f"❌ Error: Not a PostgreSQL database! Got: {engine}")
    sys.exit(1)

print(f"  ✓ Database engine: {engine}")
print(f"  ✓ Host: {railway_db.get('HOST', 'Unknown')}")
print(f"  ✓ Database: {railway_db.get('NAME', 'Unknown')}")

# Step 3: Connect to Railway and get existing users
print(f"\n[3/4] Connecting to Railway PostgreSQL...")
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
    
    # Get existing Railway users
    railway_users = User.objects.using('default').all()
    railway_usernames = {user.username for user in railway_users}
    print(f"  ✓ Found {len(railway_usernames)} existing users in Railway")
    
    if railway_usernames:
        print("  Existing Railway users:")
        for username in railway_usernames:
            print(f"    - {username}")
    
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    sys.exit(1)

# Step 4: Transfer users
print(f"\n[4/4] Transferring users to Railway PostgreSQL...")
settings.DATABASES['default'] = original_db  # Switch back to SQLite for reading

transferred = 0
skipped = 0
errors = 0

for local_user in local_users:
    try:
        # Check if user already exists in Railway
        if local_user.username in railway_usernames:
            print(f"  ⏭️  Skipping {local_user.username} (already exists)")
            skipped += 1
            continue
        
        # Create user in Railway database
        settings.DATABASES['default'] = railway_db  # Switch to Railway for writing
        
        # Create the user with all attributes
        new_user = User.objects.using('default').create(
            username=local_user.username,
            email=local_user.email,
            first_name=local_user.first_name,
            last_name=local_user.last_name,
            is_staff=local_user.is_staff,
            is_superuser=local_user.is_superuser,
            is_active=local_user.is_active,
            date_joined=local_user.date_joined,
        )
        
        # Set password (copy the hashed password)
        new_user.password = local_user.password
        new_user.save()
        
        print(f"  ✓ Transferred {local_user.username} ({'Superuser' if local_user.is_superuser else 'Regular user'})")
        transferred += 1
        
        # Switch back to SQLite for next iteration
        settings.DATABASES['default'] = original_db
        
    except Exception as e:
        print(f"  ❌ Error transferring {local_user.username}: {e}")
        errors += 1
        settings.DATABASES['default'] = original_db  # Restore on error

# Final verification
print("\n" + "=" * 70)
print("  VERIFICATION")
print("=" * 70)

settings.DATABASES['default'] = railway_db
railway_users_final = User.objects.using('default').all()
railway_count = railway_users_final.count()

print(f"\n✓ Railway PostgreSQL now has {railway_count} users:")
for user in railway_users_final:
    print(f"  - {user.username} ({user.email or 'No email'})")
    print(f"    Superuser: {user.is_superuser}, Staff: {user.is_staff}, Active: {user.is_active}")

print("\n" + "=" * 70)
print("  ✅ USER SYNC COMPLETE!")
print("=" * 70)
print(f"\nSummary:")
print(f"  - Transferred: {transferred} users")
print(f"  - Skipped: {skipped} users (already exist)")
print(f"  - Errors: {errors} users")
print(f"  - Total in Railway: {railway_count} users")

# Restore original database
settings.DATABASES['default'] = original_db

print("\n" + "=" * 70)

