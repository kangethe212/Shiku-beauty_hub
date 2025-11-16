#!/usr/bin/env python
"""
Check superusers in both localhost (SQLite) and Railway (PostgreSQL) databases
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connections
from django.conf import settings

print("=" * 70)
print("  CHECKING SUPERUSERS IN BOTH DATABASES")
print("=" * 70)

# Check localhost database (SQLite)
print("\n" + "=" * 70)
print("  LOCALHOST DATABASE (SQLite)")
print("=" * 70)

try:
    # Use default database (SQLite for local)
    local_users = User.objects.filter(is_superuser=True)
    local_count = local_users.count()
    
    print(f"\n✓ Found {local_count} superuser(s) in localhost database:")
    
    if local_count > 0:
        print("\n" + "-" * 70)
        print(f"{'Username':<20} {'Email':<30} {'Date Joined':<20}")
        print("-" * 70)
        for user in local_users:
            print(f"{user.username:<20} {user.email or 'N/A':<30} {str(user.date_joined)[:19]:<20}")
        print("-" * 70)
        
        print("\n📝 User Details:")
        for user in local_users:
            print(f"\n  Username: {user.username}")
            print(f"  Email: {user.email or 'Not set'}")
            print(f"  First Name: {user.first_name or 'Not set'}")
            print(f"  Last Name: {user.last_name or 'Not set'}")
            print(f"  Is Active: {user.is_active}")
            print(f"  Is Staff: {user.is_staff}")
            print(f"  Is Superuser: {user.is_superuser}")
            print(f"  Date Joined: {user.date_joined}")
            print(f"  Last Login: {user.last_login or 'Never'}")
            print(f"  Password Hash: {user.password[:50]}... (hashed, cannot be retrieved)")
    else:
        print("\n⚠️  No superusers found in localhost database")
        
except Exception as e:
    print(f"\n❌ Error checking localhost database: {e}")

# Check Railway database (PostgreSQL)
print("\n" + "=" * 70)
print("  RAILWAY DATABASE (PostgreSQL)")
print("=" * 70)

# Railway PostgreSQL connection string
RAILWAY_DB_URL = "postgresql://postgres:UExYLWxaerRFXJtjSNScCTrQRgJQBQZJ@yamanote.proxy.rlwy.net:27057/railway"

try:
    import dj_database_url
    railway_db = dj_database_url.config(default=RAILWAY_DB_URL)
    
    # Verify it's PostgreSQL
    if 'postgres' not in railway_db.get('ENGINE', '').lower():
        raise ValueError("Not a PostgreSQL database")
    
    # Temporarily set Railway as default
    original_db = settings.DATABASES['default']
    settings.DATABASES['railway'] = railway_db
    settings.DATABASES['default'] = railway_db
    
    # Close existing connections
    connections.close_all()
    
    # Test connection - use PostgreSQL-specific query
    conn = connections['default']
    engine = settings.DATABASES['default'].get('ENGINE', '')
    print(f"\n✓ Connected to Railway PostgreSQL")
    print(f"  Engine: {engine}")
    
    # Get superusers from Railway
    railway_users = User.objects.using('default').filter(is_superuser=True)
    railway_count = railway_users.count()
    
    print(f"\n✓ Found {railway_count} superuser(s) in Railway database:")
    
    if railway_count > 0:
        print("\n" + "-" * 70)
        print(f"{'Username':<20} {'Email':<30} {'Date Joined':<20}")
        print("-" * 70)
        for user in railway_users:
            print(f"{user.username:<20} {user.email or 'N/A':<30} {str(user.date_joined)[:19]:<20}")
        print("-" * 70)
        
        print("\n📝 User Details:")
        for user in railway_users:
            print(f"\n  Username: {user.username}")
            print(f"  Email: {user.email or 'Not set'}")
            print(f"  First Name: {user.first_name or 'Not set'}")
            print(f"  Last Name: {user.last_name or 'Not set'}")
            print(f"  Is Active: {user.is_active}")
            print(f"  Is Staff: {user.is_staff}")
            print(f"  Is Superuser: {user.is_superuser}")
            print(f"  Date Joined: {user.date_joined}")
            print(f"  Last Login: {user.last_login or 'Never'}")
            print(f"  Password Hash: {user.password[:50]}... (hashed, cannot be retrieved)")
    else:
        print("\n⚠️  No superusers found in Railway database")
        print("\n💡 To create a superuser on Railway, run:")
        print("   railway run python manage.py createsuperuser")
        
except Exception as e:
    print(f"\n❌ Error checking Railway database: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original database
    settings.DATABASES['default'] = original_db

print("\n" + "=" * 70)
print("  IMPORTANT NOTES")
print("=" * 70)
print("\n⚠️  Passwords are hashed and cannot be retrieved!")
print("   Django uses secure password hashing (PBKDF2, bcrypt, etc.)")
print("   Original passwords are never stored - only hashes")
print("\n💡 To reset a password:")
print("   1. Use Django admin: Go to Users → Select user → Change password")
print("   2. Use command line: python manage.py changepassword <username>")
print("   3. Create new superuser: python manage.py createsuperuser")
print("\n" + "=" * 70)

